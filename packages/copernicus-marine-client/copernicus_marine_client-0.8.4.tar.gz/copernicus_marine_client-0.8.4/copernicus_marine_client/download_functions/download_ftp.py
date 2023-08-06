import logging
import os
import re
from ftplib import FTP
from itertools import chain
from multiprocessing.pool import ThreadPool
from typing import Any, Optional, Tuple

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

# /////////////////////////////
# ---Using ftplib
# /////////////////////////////


def download_ftp(
    username: str,
    password: str,
    native_request: NativeRequest,
) -> str:
    message, host, filenames_in = download_header(
        str(native_request.dataset_url),
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
    groups_in_files_count = len(groups_in_files)
    download_summary_list = pool.map(
        download_files,
        zip(
            [host] * groups_in_files_count,
            [username] * groups_in_files_count,
            [password] * groups_in_files_count,
            groups_in_files,
            groups_out_files,
        ),
    )
    download_summary = "".join(map(str, download_summary_list))
    return download_summary


def download_header(
    data_path: str, regex: Optional[str], username: str, password: str
) -> Tuple[str, str, list[str]]:

    (host, path) = parse_ftp_dataset_url(data_path)
    message = "You requested the download of the following files:\n"
    total_size = 0
    with FTP(host) as ftp:
        ftp.login(user=username, passwd=password)
        raw_filenames = get_filenames_recursively(ftp, path)
        if regex:
            regex_compiled = re.compile(regex)
            filenames = list(filter(regex_compiled.match, raw_filenames))
        else:
            filenames = raw_filenames
    pool = ThreadPool()
    nfilenames_per_process, nfilenames = 100, len(filenames)
    indexes = append(
        arange(0, nfilenames, nfilenames_per_process, dtype=int),
        nfilenames,
    )
    groups_filenames = [
        filenames[indexes[i] : indexes[i + 1]] for i in range(len(indexes) - 1)
    ]
    results = pool.map(
        get_filename_size_tuple,
        zip(
            [host] * len(groups_filenames),
            [username] * len(groups_filenames),
            [password] * len(groups_filenames),
            groups_filenames,
        ),
    )
    flattened_results = list(chain(*results))
    total_size += sum([int(res[1]) for res in flattened_results])
    for result in flattened_results[:20]:
        message += str(result[0])
        message += f" - {format_file_size(float(result[1]))}\n"
    if len(flattened_results) > 20:
        message += f"Printed 20 out of {len(flattened_results)} files\n"
    message += (
        f"\nTotal size of the download: {format_file_size(total_size)}\n\n"
    )
    return (message, host, filenames)


def get_filenames_recursively(
    ftp: FTP, path: str, extensions: list[str] = [".nc"]
) -> list[str]:
    if any(extension in path for extension in extensions):
        # path is a file
        return [path]
    elif len(ftp.nlst(path)) == 0:
        # empty dir
        return []
    elif ftp.nlst(path)[0] == path:
        # path is a file
        return [path]
    else:
        # path is a dir
        return [
            filename
            for element in ftp.nlst(path)
            for filename in get_filenames_recursively(ftp, element)
        ]


def get_filename_size_tuple(
    tuple_ftp_filename: Tuple[str, str, str, list[str]]
) -> list[Tuple[str, Any]]:
    host, username, password, filenames = tuple_ftp_filename
    with FTP(host) as ftp:
        ftp.login(user=username, passwd=password)
        list_tuples = [
            (filename, ftp.size(filename)) for filename in filenames
        ]
    return list_tuples


def download_files(
    tuple_ftp_filename: Tuple[str, str, str, list[str], list[str]],
) -> str:
    def _ftp_file_download(ftp, file_in, file_out):
        """
        Download ONE file and return a string of the result
        """
        os.makedirs(os.path.dirname(file_out), exist_ok=True)
        with open(file_out, "wb") as fp:
            size = ftp.size(file_in)
            with tqdm(
                total=size,
                unit_scale=True,
                desc=file_in.split("/")[-1],
            ) as pbar:

                def callback(data):
                    pbar.update(len(data))
                    fp.write(data)

                res = ftp.retrbinary(f"RETR {file_in}", callback)
            if not res.startswith("226 Transfer complete"):
                logging.error(f"Download {file_in} failed")
                if os.path.isfile(file_out):
                    os.remove(file_out)
                summary_string = f"Could not download {file_in}!\n"
            else:
                summary_string = f"File {file_out} created\n"
        return summary_string

    host, username, password, filenames_in, filenames_out = tuple_ftp_filename
    download_summary = ""
    with FTP(host) as ftp:
        ftp.login(user=username, passwd=password)
        for file_in, file_out in zip(filenames_in, filenames_out):
            download_summary += _ftp_file_download(ftp, file_in, file_out)
    return download_summary


# /////////////////////////////
# --- Tools
# /////////////////////////////


def parse_ftp_dataset_url(data_path: str) -> tuple[str, str]:
    host = data_path[len("ftp://") :].split("/")[0]
    path = data_path[len("ftp://" + host + "/") :]
    return (host, path)


def create_filenames_out(
    filenames_in: list[str],
    overwrite: bool,
    output_directory: str = "",
    no_directories=False,
) -> list[str]:
    filenames_out = []
    for filename_in in filenames_in:
        filename_out = f"{output_directory}{os.sep}"
        if no_directories:
            filename_out += filename_in.split(os.sep)[-1]
        elif filename_in.startswith("Core/"):
            filename_out += filename_in[len("Core/") :]

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
