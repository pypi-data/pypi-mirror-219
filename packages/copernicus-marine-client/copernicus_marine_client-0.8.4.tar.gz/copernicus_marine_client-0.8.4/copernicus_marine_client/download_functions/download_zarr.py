import logging
import os
from datetime import datetime
from os import path
from typing import Optional

import click
import xarray as xr
import zarr

from copernicus_marine_client.catalogue_parser.request_structure import (
    SubsetRequest,
)
from copernicus_marine_client.download_functions.subset_xarray import subset
from copernicus_marine_client.utils import (
    FORCE_DOWNLOAD_CLI_PROMPT_MESSAGE,
    get_unique_filename,
)


def get_optimized_chunking(subset_request: SubsetRequest) -> str:
    """Function to calculate the optimized type of chunking,
    based on a subset_request.
    Returns a str: "map" if time-chunking is optimized,
    "timeserie" if geo-chunking is optimized
    """
    logging.info(
        "THIS CHUNKING OPTIMIZATION FUNCTION IS "
        + "A PLACEHOLDER, DO NOT RELY ON IT!!"
    )
    chunking_selected = "map"
    if (
        isinstance(subset_request.minimal_latitude, float)
        and isinstance(subset_request.maximal_latitude, float)
        and isinstance(subset_request.minimal_longitude, float)
        and isinstance(subset_request.maximal_longitude, float)
    ):
        surface = abs(
            subset_request.maximal_longitude - subset_request.minimal_longitude
        ) * abs(
            subset_request.maximal_latitude - subset_request.minimal_latitude
        )

        if surface < 20:
            chunking_selected = "timeserie"
    return chunking_selected


def download_dataset(
    username: str,
    password: str,
    geographical_subset: Optional[
        tuple[
            Optional[float], Optional[float], Optional[float], Optional[float]
        ]
    ],
    temporal_subset: Optional[tuple[Optional[datetime], Optional[datetime]]],
    depth_range: Optional[tuple[Optional[float], Optional[float]]],
    dataset_url: str,
    output_directory: str,
    output_filename: str,
    variables: Optional[list[str]],
    force_download: bool = False,
    overwrite: bool = False,
):

    dataset = xr.open_zarr(dataset_url)
    dataset = subset(
        dataset, variables, geographical_subset, temporal_subset, depth_range
    )
    dataset = dataset.chunk(chunks="auto")

    output_path = path.join(output_directory, output_filename)

    if not force_download:
        logger = logging.getLogger("blank_logger")
        logger.warn(dataset)
        click.confirm(
            FORCE_DOWNLOAD_CLI_PROMPT_MESSAGE, abort=True, default=True
        )

    if os.path.exists(output_path):
        if not overwrite:
            output_filename = get_unique_filename(filepath=output_path)
            output_path = path.join(output_directory, output_filename)

    write_mode = "w"
    if output_filename.endswith(".nc"):
        if not os.path.isdir(output_directory):
            os.makedirs(output_directory)
        dataset.to_netcdf(output_path, mode=write_mode)
    else:
        store = zarr.DirectoryStore(output_path)
        dataset.to_zarr(store=store, mode=write_mode)

    logging.info(f"Successfully downloaded to {output_path}")


def download_zarr(
    username: str,
    password: str,
    subset_request: SubsetRequest,
):

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
    dataset_url = str(subset_request.dataset_url)
    output_directory = (
        subset_request.output_directory
        if subset_request.output_directory
        else "."
    )
    output_filename = (
        subset_request.output_filename
        if subset_request.output_filename
        else "data.zarr"
    )
    variables = subset_request.variables
    force_download = subset_request.force_download

    download_dataset(
        username=username,
        password=password,
        geographical_subset=geographical_subset,
        temporal_subset=temporal_subset,
        depth_range=depth_range,
        dataset_url=dataset_url,
        output_directory=output_directory,
        output_filename=output_filename,
        variables=variables,
        force_download=force_download,
        overwrite=subset_request.overwrite,
    )
    return path.join(output_directory, output_filename)
