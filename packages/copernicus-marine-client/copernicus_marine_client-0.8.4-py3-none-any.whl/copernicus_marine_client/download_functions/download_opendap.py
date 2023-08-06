import itertools
import logging
import os
import re
from datetime import datetime
from http.client import IncompleteRead
from typing import List, Optional, Tuple

import click
import requests
import xarray as xr
from dask.diagnostics import ProgressBar
from pydap.net import HTTPError
from xarray.backends import PydapDataStore

from copernicus_marine_client.catalogue_parser.request_structure import (
    SubsetRequest,
)
from copernicus_marine_client.download_functions.subset_xarray import subset
from copernicus_marine_client.utils import (
    FORCE_DOWNLOAD_CLI_PROMPT_MESSAGE,
    get_unique_filename,
)


def __parse_limit(message: str) -> Optional[float]:
    match = re.search(r", max=.+\";", message)
    if match:
        limit = match.group().strip(', max=";')
        return float(limit)
    else:
        return None


def split_by_chunks(dataset):
    chunk_slices = {}
    for dim, chunks in dataset.chunks.items():
        slices = []
        start = 0
        for chunk in chunks:
            if start >= dataset.sizes[dim]:
                break
            stop = start + chunk
            slices.append(slice(start, stop))
            start = stop
        chunk_slices[dim] = slices
    for slices in itertools.product(*chunk_slices.values()):
        selection = dict(zip(chunk_slices.keys(), slices))
        yield dataset[selection]


def find_chunk(ds: xr.Dataset, limit: float) -> Optional[int]:
    N = ds["time"].shape[0]
    for i in range(N, 0, -1):
        ds = ds.chunk({"time": i})
        ts = list(split_by_chunks(ds))
        if (ts[0].nbytes / (1000 * 1000)) < limit:
            return i
    return None


def chunked_download(
    store: PydapDataStore,
    dataset: xr.Dataset,
    limit: Optional[int],
    error: HTTPError,
    output_directory: str,
    output_filename: str,
    variables: Optional[List[str]] = None,
    geographical_subset: Optional[
        Tuple[
            Optional[float], Optional[float], Optional[float], Optional[float]
        ]
    ] = None,
    temporal_subset: Optional[
        Tuple[Optional[datetime], Optional[datetime]]
    ] = None,
    depth_range: Optional[Tuple[Optional[float], Optional[float]]] = None,
):
    filepath = os.path.join(output_directory, output_filename)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except OSError:
            logging.error("Error while deleting file: ", filepath)

    logging.info("Dataset must be chunked.")
    if limit is None:
        size_limit = __parse_limit(str(error.comment))
    else:
        size_limit = limit

    if size_limit:
        logging.info(f"Server download limit is {size_limit} MB")
        i_chunk = find_chunk(dataset, size_limit)
        dataset = xr.open_dataset(
            store, mask_and_scale=True, chunks={"time": i_chunk}
        )

        dataset = subset(
            dataset,
            variables,
            geographical_subset,
            temporal_subset,
            depth_range,
        )

        dataset_slices = list(split_by_chunks(dataset))

        slice_paths = [
            os.path.join(output_directory, str(dataset_slice) + ".nc")
            for dataset_slice in range(len(dataset_slices))
        ]

        logging.info("Downloading " + str(len(dataset_slices)) + " files...")
        delayed = xr.save_mfdataset(
            datasets=dataset_slices, paths=slice_paths, compute=False
        )
        with ProgressBar():
            delayed.compute()
        logging.info("Files downloaded")

        if output_filename is not None:
            logging.info(f"Concatenating files into {output_filename}...")
            dataset = xr.open_mfdataset(slice_paths)
            delayed = dataset.to_netcdf(filepath, compute=False)
            with ProgressBar():
                delayed.compute()
            logging.info("Files concatenated")

            logging.info("Removing temporary files")
            for path in slice_paths:
                try:
                    os.remove(path)
                except OSError:
                    logging.error("Error while deleting file: ", path)
            logging.info("Done")

    else:
        logging.info("No limit found in the returned server error")


def download_dataset(
    username: str,
    password: str,
    dataset_url: str,
    output_directory: str,
    output_filename: str,
    variables: Optional[List[str]],
    geographical_subset: Optional[
        Tuple[
            Optional[float], Optional[float], Optional[float], Optional[float]
        ]
    ],
    temporal_subset: Optional[Tuple[Optional[datetime], Optional[datetime]]],
    depth_range: Optional[Tuple[Optional[float], Optional[float]]],
    limit: Optional[int],
    confirmation: Optional[bool],
    overwrite: Optional[bool],
):
    def _open_subset(
        username: str,
        password: str,
        dataset_url: str,
        variables: Optional[list[str]],
        geographical_subset: Optional[
            Tuple[
                Optional[float],
                Optional[float],
                Optional[float],
                Optional[float],
            ]
        ],
        temporal_subset: Optional[
            Tuple[Optional[datetime], Optional[datetime]]
        ],
        depth_range: Optional[Tuple[Optional[float], Optional[float]]],
    ) -> xr.Dataset:
        session = requests.Session()
        session.auth = (username, password)
        try:
            store = PydapDataStore.open(
                dataset_url, session=session, timeout=300
            )
        except IncompleteRead:
            raise ConnectionError(
                "Unable to retrieve data through opendap.\n"
                "This error usually comes from wrong credentials."
            )

        dataset = xr.open_dataset(store)
        dataset = subset(
            dataset,
            variables,
            geographical_subset,
            temporal_subset,
            depth_range,
        )
        return dataset, store

    dataset, store = _open_subset(
        username,
        password,
        dataset_url,
        variables,
        geographical_subset,
        temporal_subset,
        depth_range,
    )

    complete_dataset = os.path.join(output_directory, output_filename)

    if confirmation:
        logger = logging.getLogger("blank_logger")
        logger.warn(dataset)
        click.confirm(
            FORCE_DOWNLOAD_CLI_PROMPT_MESSAGE, abort=True, default=True
        )

    if os.path.exists(complete_dataset):
        if not overwrite:
            output_filename = get_unique_filename(filepath=complete_dataset)
            complete_dataset = os.path.join(output_directory, output_filename)

    write_mode = "w"

    try:
        logging.info("Trying to download as one file...")
        dataset.to_netcdf(complete_dataset, mode=write_mode)
        logging.info(f"Successfully downloaded to {complete_dataset}")
    except HTTPError as error:
        chunked_download(
            store,
            dataset,
            limit,
            error,
            output_directory,
            output_filename,
            variables,
            geographical_subset,
            temporal_subset,
            depth_range,
        )


def download_opendap(
    username: str,
    password: str,
    subset_request: SubsetRequest,
) -> str:
    if subset_request.dataset_url is None:
        e = ValueError("Dataset url is required at this stage")
        logging.error(e)
        raise e
    else:
        dataset_url = subset_request.dataset_url
    geographical_subset = (
        subset_request.minimal_latitude,
        subset_request.maximal_latitude,
        subset_request.minimal_longitude,
        subset_request.maximal_longitude,
    )
    temporal_subset = (
        subset_request.start_datetime,
        subset_request.end_datetime,
    )
    depth_range = (subset_request.minimal_depth, subset_request.maximal_depth)

    output_directory = (
        subset_request.output_directory
        if subset_request.output_directory
        else "."
    )
    output_filename = (
        subset_request.output_filename
        if subset_request.output_filename
        else "data.nc"
    )
    limit = False
    download_dataset(
        username=username,
        password=password,
        dataset_url=dataset_url,
        output_directory=output_directory,
        output_filename=output_filename,
        variables=subset_request.variables,
        geographical_subset=geographical_subset,
        temporal_subset=temporal_subset,
        depth_range=depth_range,
        limit=limit,
        confirmation=not subset_request.force_download,
        overwrite=subset_request.overwrite,
    )
    return os.path.join(output_directory, output_filename)
