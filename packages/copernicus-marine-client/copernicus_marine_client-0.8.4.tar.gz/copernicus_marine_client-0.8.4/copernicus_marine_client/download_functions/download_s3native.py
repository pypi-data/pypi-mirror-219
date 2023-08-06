import logging
import os
import re
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import Optional, Tuple

import boto3
import botocore
import click
from numpy import append, arange
from tqdm import tqdm

from copernicus_marine_client.catalogue_parser.request_structure import (
    NativeRequest,
)
from copernicus_marine_client.utils import (
    FORCE_DOWNLOAD_CLI_PROMPT_MESSAGE,
    get_unique_filename,
)

MARINE_DATA_LAKE_LISTING_ENDPOINT = "https://marine.copernicus.eu"
MARINE_DATA_LAKE_LISTING_NATIVE_BUCKET = "mdl-native-list"
MARINE_DATA_LAKE_DOWNLOAD_NATIVE_BUCKET = "mdl-native"
MARINE_DATA_LAKE_S3_LISTING_NATIVE_ROOT_URI = (
    f"{MARINE_DATA_LAKE_LISTING_NATIVE_BUCKET}/native"
)
MARINE_DATA_LAKE_S3_DOWNLOAD_NATIVE_ROOT_URI = (
    f"{MARINE_DATA_LAKE_DOWNLOAD_NATIVE_BUCKET}/native"
)


def download_s3native(
    username: str,
    password: str,
    native_request: NativeRequest,
) -> str:
    message, endpoint_url, filenames_in = download_header(
        [str(native_request.dataset_url)],
        native_request.regex,
        username,
        password,
    )
    filenames_out = create_filenames_out(
        filenames_in=filenames_in,
        output_directory=native_request.output_directory,
        no_directories=native_request.no_directories,
        overwrite=native_request.overwrite,
    )
    logging.info(message)
    if native_request.show_outputnames:
        logging.info("Output filenames:")
        for filename_out in filenames_out:
            logging.info(filename_out)
    if not native_request.force_download:
        click.confirm(FORCE_DOWNLOAD_CLI_PROMPT_MESSAGE, abort=True)

    pool = ThreadPool()
    nfiles_per_process, nfiles = 1, len(filenames_in)
    indexes = append(
        arange(0, nfiles, nfiles_per_process, dtype=int),
        nfiles,
    )
    groups_in_files = [
        filenames_in[indexes[i] : indexes[i + 1]]
        for i in range(len(indexes) - 1)
    ]
    groups_out_files = [
        filenames_out[indexes[i] : indexes[i + 1]]
        for i in range(len(indexes) - 1)
    ]

    for groups_out_file in groups_out_files:
        parent_dir = Path(groups_out_file[0]).parent
        if not os.path.isdir(parent_dir):
            os.makedirs(parent_dir)

    download_summary_list = pool.imap(
        download_files,
        zip(
            [endpoint_url] * len(groups_in_files),
            groups_in_files,
            groups_out_files,
        ),
    )
    list(tqdm(download_summary_list, total=len(groups_in_files)))
    download_summary = "Download complete"
    return download_summary


def download_header(
    data_paths: list[str], regex: Optional[str], username: str, password: str
) -> Tuple[str, str, list[str]]:
    path_dict = parse_s3native_dataset_url(data_paths)
    message = "You requested the download of the following files:\n"
    filenames, sizes, total_size = [], [], 0.0
    for endpoint_url, paths in path_dict.items():
        for path in paths:
            raw_filenames = list_files_on_marine_data_lake_s3(path)
            filename_filtered = []
            for filename, size in raw_filenames:
                if not regex or re.match(regex, filename):
                    filenames += [filename]
                    sizes += [float(size)]
                    total_size += float(size)
                    filename_filtered.append((filename, size))

    for filename, size in filename_filtered[:20]:
        message += str(filename)
        message += f" - {format_file_size(float(size))}\n"
    if len(filenames) > 20:
        message += f"Printed 20 out of {len(filenames)} files\n"
    message += (
        f"\nTotal size of the download: {format_file_size(total_size)}\n\n"
    )
    return (message, endpoint_url, filenames)


def list_files_on_marine_data_lake_s3(
    path: str,
    files_already_found: list[tuple[str, int]] = [],
) -> list[tuple[str, int]]:
    # In order to list S3 native files, we are using CDN functionnalities using the following endpoint_url and path  # noqa
    path = path.replace(
        f"s3://{MARINE_DATA_LAKE_S3_DOWNLOAD_NATIVE_ROOT_URI}",
        f"s3://{MARINE_DATA_LAKE_S3_LISTING_NATIVE_ROOT_URI}",
    )

    if not path.endswith("/"):
        path += "/"

    s3_service_resource = boto3.resource(
        "s3",
        config=botocore.config.Config(
            # Configures to use subdomain/virtual calling format.
            s3={"addressing_style": "virtual"},
            signature_version=botocore.UNSIGNED,
        ),
        endpoint_url=MARINE_DATA_LAKE_LISTING_ENDPOINT,
    )
    s3_bucket = s3_service_resource.Bucket(
        name=MARINE_DATA_LAKE_LISTING_NATIVE_BUCKET
    )
    prefix = path.replace(
        f"s3://{MARINE_DATA_LAKE_LISTING_NATIVE_BUCKET}/", ""
    )
    s3_filter = s3_bucket.objects.filter(Prefix=prefix, Delimiter="/")

    for file in s3_filter:
        files_already_found.extend(
            [
                (
                    f"s3://{MARINE_DATA_LAKE_DOWNLOAD_NATIVE_BUCKET}/"
                    + file.key,
                    file.size,
                )
            ]
        )
    return files_already_found


def download_files(
    tuple_s3native_filename: Tuple[str, list[str], list[str]],
) -> str:
    def _s3native_file_download(
        endpoint_url: str, file_in: str, file_out: str
    ) -> str:
        """
        Download ONE file and return a string of the result
        """
        s3_service_resource = boto3.resource(
            "s3",
            config=botocore.config.Config(
                # Configures to use subdomain/virtual calling format.
                s3={"addressing_style": "virtual"},
                signature_version=botocore.UNSIGNED,
            ),
            endpoint_url=endpoint_url,
        )

        s3_service_resource.meta.client.download_file(
            MARINE_DATA_LAKE_DOWNLOAD_NATIVE_BUCKET,
            file_in.replace("s3://mdl-native/", ""),
            file_out,
        )

        return f"File {file_out} created\n"

    endpoint_url, filenames_in, filenames_out = tuple_s3native_filename
    download_summary = ""
    for file_in, file_out in zip(filenames_in, filenames_out):
        download_summary += _s3native_file_download(
            endpoint_url, file_in, file_out
        )
    return download_summary


# /////////////////////////////
# --- Tools
# /////////////////////////////


def parse_s3native_dataset_url(data_paths: list[str]) -> dict:
    path_dict: dict[str, list[str]] = {}
    for data_path in data_paths:
        endpoint_url, path = data_path.split("/mdl-native/", maxsplit=1)
        path = "s3://mdl-native/" + path
        path_dict.setdefault(endpoint_url, []).append(path)
    return path_dict


def create_filenames_out(
    filenames_in: list[str],
    overwrite: bool,
    output_directory: str = "",
    no_directories=False,
) -> list[str]:
    filenames_out = []
    for filename_in in filenames_in:
        filename_out = f"{output_directory}/"
        if no_directories:
            filename_out += filename_in.split("/")[-1]
        elif filename_in.startswith(
            f"s3://{MARINE_DATA_LAKE_S3_DOWNLOAD_NATIVE_ROOT_URI}{os.sep}"
        ):
            filename_out += filename_in.split(
                f"s3://{MARINE_DATA_LAKE_S3_DOWNLOAD_NATIVE_ROOT_URI}{os.sep}"
            )[-1]
        elif filename_in.startswith(
            f"s3://{MARINE_DATA_LAKE_S3_LISTING_NATIVE_ROOT_URI}{os.sep}"
        ):
            filename_out += filename_in.split(
                f"s3://{MARINE_DATA_LAKE_S3_LISTING_NATIVE_ROOT_URI}{os.sep}"
            )[-1]

        if os.path.exists(filename_out):
            if not overwrite:
                filename_out = get_unique_filename(filepath=filename_out)

        filenames_out.append(filename_out)
    return filenames_out


def format_file_size(
    size: float, decimals: int = 2, binary_system: bool = False
) -> str:
    if binary_system:
        units: list[str] = [
            "B",
            "KiB",
            "MiB",
            "GiB",
            "TiB",
            "PiB",
            "EiB",
            "ZiB",
        ]
        largest_unit: str = "YiB"
        step: int = 1024
    else:
        units = ["B", "kB", "MB", "GB", "TB", "PB", "EB", "ZB"]
        largest_unit = "YB"
        step = 1000

    for unit in units:
        if size < step:
            return ("%." + str(decimals) + "f %s") % (size, unit)
        size /= step

    return ("%." + str(decimals) + "f %s") % (size, largest_unit)
