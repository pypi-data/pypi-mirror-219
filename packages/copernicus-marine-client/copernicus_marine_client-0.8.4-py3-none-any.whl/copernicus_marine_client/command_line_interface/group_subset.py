import logging
import logging.config
import os
from datetime import datetime
from typing import Any, List, Literal, Optional

import click
import xarray as xr
import zarr

from copernicus_marine_client.catalogue_parser.catalogue_parser import (
    GEOCHUNKED_KEY,
    MOTU_KEY,
    OPENDAP_KEY,
    TIMECHUNKED_KEY,
    get_dataset_url_from_id,
    get_protocol_from_url,
    parse_catalogue,
)
from copernicus_marine_client.catalogue_parser.request_structure import (
    SubsetRequest,
    convert_motu_api_request_to_structure,
    subset_request_from_file,
)
from copernicus_marine_client.command_line_interface.group_login import (
    get_username_password,
)
from copernicus_marine_client.download_functions.download_motu import (
    download_motu,
)
from copernicus_marine_client.download_functions.download_opendap import (
    download_opendap,
)
from copernicus_marine_client.download_functions.download_zarr import (
    download_zarr,
    get_optimized_chunking,
)
from copernicus_marine_client.utils import (
    OVERWRITE_LONG_OPTION,
    OVERWRITE_OPTION_HELP_TEXT,
    OVERWRITE_SHORT_OPTION,
)

PROTOCOL_KEYS_ORDER = {
    "zarr": (TIMECHUNKED_KEY, GEOCHUNKED_KEY),
    "zarr-map": TIMECHUNKED_KEY,
    "zarr-timeserie": GEOCHUNKED_KEY,
    "opendap": OPENDAP_KEY,
    "motu": MOTU_KEY,
}

CREDENTIALS_REQUIRED_PROTOCOLS = [
    "opendap",
    "motu",
]


@click.group()
def cli_group_subset() -> None:
    pass


@cli_group_subset.command(
    "subset",
    short_help="Downloads subsets of datasets as NetCDF files or Zarr stores",
    help="""
    Downloads subsets of datasets as NetCDF files or Zarr stores.
    Either one of 'dataset-id' or 'dataset-url' is required (can be found via the 'copernicus-marine describe' command).
    The arguments value passed individually through the CLI take precedence over the values from the "motu-api-request" option,
    which takes precedence over the ones from the "request-file" option

    Example:

    \b
    > copernicus-marine subset
    --dataset-id METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2
    --variable analysed_sst --variable sea_ice_fraction
    --start-datetime 2021-01-01 --end-datetime 2021-01-02
    --minimal-longitude 0.0 --maximal-longitude 0.1
    --minimal-latitude 0.0 --maximal-latitude 0.1

    \b
    > copernicus-marine subset -i METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2 -v analysed_sst -v sea_ice_fraction -t 2021-01-01 -T 2021-01-02 -x 0.0 -X 0.1 -y 0.0 -Y 0.1
    """,  # noqa
)
@click.option(
    "--dataset-url",
    "-u",
    type=str,
    help="The full dataset URL",
)
@click.option(
    "--dataset-id",
    "-i",
    type=str,
    help="The dataset id",
)
@click.option(
    "--username",
    type=str,
    envvar="COPERNICUS_MARINE_SERVICE_USERNAME",
    default=None,
    help="If not set, search for environment variable"
    + " COPERNICUS_MARINE_SERVICE_USERNAME"
    + ", or else look for configuration files, or else ask for user input",
)
@click.option(
    "--password",
    type=str,
    envvar="COPERNICUS_MARINE_SERVICE_PASSWORD",
    default=None,
    help="If not set, search for environment variable"
    + " COPERNICUS_MARINE_SERVICE_PASSWORD"
    + ", or else look for configuration files, or else ask for user input",
)
@click.option(
    "--variable",
    "-v",
    "variables",
    type=str,
    help="Specify dataset variables",
    multiple=True,
)
@click.option(
    "--minimal-longitude",
    "-x",
    type=click.FloatRange(min=-180, max=180),
    help="Minimal longitude for the subset. Requires a float within this range:",
)
@click.option(
    "--maximal-longitude",
    "-X",
    type=click.FloatRange(min=-180, max=180),
    help="Maximal longitude for the subset. Requires a float within this range:",
)
@click.option(
    "--minimal-latitude",
    "-y",
    type=click.FloatRange(min=-90, max=90),
    help="Minimal latitude for the subset. Requires a float within this range:",
)
@click.option(
    "--maximal-latitude",
    "-Y",
    type=click.FloatRange(min=-90, max=90),
    help="Maximal latitude for the subset. Requires a float within this range:",
)
@click.option(
    "--minimal-depth",
    "-z",
    type=click.FloatRange(min=0),
    help="Minimal depth for the subset. Requires a float within this range:",
)
@click.option(
    "--maximal-depth",
    "-Z",
    type=click.FloatRange(min=0),
    help="Maximal depth for the subset. Requires a float within this range:",
)
@click.option(
    "--start-datetime",
    "-t",
    type=click.DateTime(
        ["%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]
    ),
    help="The start datetime of the temporal subset. Caution: encapsulate date "
    + 'with " " to ensure valid expression for format "%Y-%m-%d %H:%M:%S"',
)
@click.option(
    "--end-datetime",
    "-T",
    type=click.DateTime(
        ["%Y", "%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]
    ),
    help="The end datetime of the temporal subset. Caution: encapsulate date "
    + 'with " " to ensure valid expression for format "%Y-%m-%d %H:%M:%S"',
)
@click.option(
    "--output-directory",
    "-o",
    type=click.Path(),
    help="The destination folder for the downloaded files."
    + " Default is the current directory",
)
@click.option(
    "--config-file-directory",
    type=str,
    default=os.path.join(os.path.expanduser("~"), ".copernicus_marine_client"),
    help="Path to a directory where a configuration file is stored. Accepts "
    + ".copernicus_marine_client_credentials / .netrc or _netrc / "
    + ".motuclient-python.ini files",
)
@click.option(
    "--output-filename",
    "-f",
    type=click.Path(),
    help=(
        "Concatenate the downloaded data in the given file name "
        "(under the output directory). If "
        "the output-filename argument ends with '.nc' suffix, the file will be "
        "downloaded as a netCDF file."
    ),
)
@click.option(
    "--force-download",
    is_flag=True,
    default=False,
    help="Flag to skip confirmation before download",
)
@click.option(
    OVERWRITE_LONG_OPTION,
    OVERWRITE_SHORT_OPTION,
    is_flag=True,
    default=False,
    help=OVERWRITE_OPTION_HELP_TEXT,
)
@click.option(
    "--force-protocol",
    type=click.Choice(list(PROTOCOL_KEYS_ORDER.keys())),
    help="Force download through one of the available protocols",
)
@click.option(
    "--request-file",
    type=click.Path(),
    help="Option to pass a filename corresponding to a file containg CLI arguments. "
    "The file MUST follow the structure of dataclass 'SubsetRequest'. ",
)
@click.option(
    "--motu-api-request",
    type=str,
    help=(
        "Option to pass a complete MOTU api request as a string. "
        'Caution, user has to replace double quotes " with single '
        "quotes ' in the request"
    ),
)
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL", "QUIET"]),
    default="INFO",
    help=(
        "Set the details printed to console by the command "
        "(based on standard logging library)."
    ),
)
def subset(
    dataset_url: str,
    dataset_id: str,
    username: str,
    password: str,
    variables: Optional[List[str]],
    minimal_longitude: Optional[float],
    maximal_longitude: Optional[float],
    minimal_latitude: Optional[float],
    maximal_latitude: Optional[float],
    minimal_depth: Optional[float],
    maximal_depth: Optional[float],
    start_datetime: Optional[datetime],
    end_datetime: Optional[datetime],
    output_filename: Optional[str],
    force_protocol: Optional[str],
    request_file: Optional[str],
    output_directory: str,
    config_file_directory: str,
    motu_api_request: Optional[str],
    force_download: bool = False,
    overwrite_output_data: bool = False,
    log_level: str = "INFO",
):
    if log_level == "QUIET":
        logging.root.disabled = True
        logging.root.setLevel(level="CRITICAL")
    else:
        logging.root.setLevel(level=log_level)
    subset_request = SubsetRequest()
    if request_file:
        subset_request = subset_request_from_file(request_file)
    if motu_api_request:
        motu_api_subset_request = convert_motu_api_request_to_structure(
            motu_api_request
        )
        subset_request.update(motu_api_subset_request.__dict__)
    request_update_dict = {
        "dataset_url": dataset_url,
        "dataset_id": dataset_id,
        "variables": variables,
        "minimal_longitude": minimal_longitude,
        "maximal_longitude": maximal_longitude,
        "minimal_latitude": minimal_latitude,
        "maximal_latitude": maximal_latitude,
        "minimal_depth": minimal_depth,
        "maximal_depth": maximal_depth,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "output_directory": output_directory,
        "output_filename": output_filename,
        "force_protocol": force_protocol,
    }
    subset_request.update(request_update_dict)
    # Specific treatment for default values:
    # In order to not overload arguments with default values
    if force_download:
        subset_request.force_download = force_download
    if overwrite_output_data:
        subset_request.overwrite = overwrite_output_data

    subset_function(
        username,
        password,
        subset_request,
        config_file_directory,
    )


def subset_function(
    username: str,
    password: str,
    subset_request: SubsetRequest,
    config_file_directory: str = os.path.join(
        os.path.expanduser("~"), ".copernicus_marine_client"
    ),
) -> str:
    def _flatten(x):
        if isinstance(x, (tuple, list)):
            return [a for i in x for a in _flatten(i)]
        else:
            return [x]

    catalogue = parse_catalogue()
    # ---Protocol section
    possible_protocols = (
        [p for p in list(PROTOCOL_KEYS_ORDER.values()) if isinstance(p, str)]
        if not subset_request.force_protocol
        else _flatten(PROTOCOL_KEYS_ORDER[subset_request.force_protocol])
    )
    if subset_request.force_protocol:
        logging.info(
            f"You forced selection of protocol: {subset_request.force_protocol}"
        )
    if not subset_request.dataset_url:
        if not subset_request.dataset_id:
            syntax_error = SyntaxError(
                "Must specify at least one of 'dataset_url' or 'dataset_id'"
            )
            logging.error(syntax_error)
            raise syntax_error
        protocol_keys_iterator = iter(possible_protocols)
        while not subset_request.dataset_url:
            try:
                protocol = next(protocol_keys_iterator)
            except StopIteration:
                key_error = KeyError(
                    f"Dataset {subset_request.dataset_id} does "
                    "not have a valid protocol "
                    f"for subset function. Available protocols: {possible_protocols}"
                )
                logging.error(key_error)
                raise key_error
            subset_request.dataset_url = get_dataset_url_from_id(
                catalogue, subset_request.dataset_id, protocol
            )
    else:
        protocol = get_protocol_from_url(subset_request.dataset_url)
    username, password = get_username_password(
        username,
        password,
        config_file_directory,
    )
    # --- Download redirection by protocol
    if subset_request.force_protocol and (
        protocol != PROTOCOL_KEYS_ORDER[subset_request.force_protocol]
        and protocol not in PROTOCOL_KEYS_ORDER[subset_request.force_protocol]
    ):
        attribute_error = AttributeError(
            f"Dataset url ({subset_request.dataset_url}) does not match forced "
            f"protocol ({PROTOCOL_KEYS_ORDER[subset_request.force_protocol]})!"
        )
        logging.error(attribute_error)
        raise attribute_error
    elif protocol in [TIMECHUNKED_KEY, GEOCHUNKED_KEY]:
        # Check if both timechunked and geochunked data are available
        url_timechunked, url_geochunked = (
            map(
                get_dataset_url_from_id,
                [catalogue] * 2,
                [subset_request.dataset_id] * 2,
                [TIMECHUNKED_KEY, GEOCHUNKED_KEY],
            )
            if subset_request.dataset_id
            else (None, None)
        )
        if (
            url_timechunked
            and url_geochunked
            and (subset_request.force_protocol in [None, "zarr"])
        ):
            subset_request.dataset_url = (
                url_timechunked
                if get_optimized_chunking(subset_request)
                else url_geochunked
            )
        logging.info("Download Zarr files through S3")
        output_name = download_zarr(
            username,
            password,
            subset_request,
        )

    elif protocol == OPENDAP_KEY:
        logging.info("Download through OPeNDAP")
        output_name = download_opendap(
            username,
            password,
            subset_request,
        )
    elif protocol == MOTU_KEY:
        logging.info("Download through MOTU")
        output_name = download_motu(
            username,
            password,
            subset_request,
            catalogue=catalogue,
        )
    elif not protocol:
        key_error = KeyError(
            f"The requested dataset '{subset_request.dataset_id}' does not have "
            f"{possible_protocols} url available"
        )
        logging.error(key_error)
        raise
    else:
        key_error = KeyError(
            f"Protocol {protocol} not handled by subset command"
        )
        logging.error(key_error)
        raise key_error
    return output_name


def open_dataset(
    filepath: Optional[str] = None,
    engine: Literal["netcdf4", "h5netcdf", "pydap", "zarr", None] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    subset_request: Optional[SubsetRequest] = None,
    out_type: Literal["xarray", "zarr", "pandas"] = "xarray",
) -> Any:
    """
    Function to open a dataset as a python object.
    Input:
    Either the path to a dataset or a SubsetRequest with the information
    necessary to download a dataset.
    The user may need to specify the "engine" needed by xarray to open the dataset.
    Output:
    Return the dataset as either:
        - a xarray dataset
        - a zarr ZarrStore object
        - a pandas dataframe
    """

    def _open_dataset_as_xarray(
        filepath: Optional[str],
        username: Optional[str],
        password: Optional[str],
        subset_request: Optional[SubsetRequest],
        engine: Literal["netcdf4", "h5netcdf", "pydap", "zarr", None],
    ) -> xr.Dataset:
        if filepath:
            if filepath.split(".")[-1] == "nc" and engine is None:
                engine = "netcdf4"
            elif filepath.split(".")[-1] == "zarr" and engine is None:
                engine = "zarr"
            elif engine is None:
                name_error = NameError(
                    f"Dataset name ({filepath}) has non-explicit or unmapped extension "
                    "please specify an engine to open it."
                )
                logging.error(name_error)
                raise name_error
            store_name = filepath.rsplit(".", maxsplit=1)[0] + ".zarr"
            dataset = xr.open_dataset(filepath, engine=engine)
        elif subset_request and username and password:
            output_name = subset_function(username, password, subset_request)
            if output_name.split(".")[-1] == "nc" and engine is None:
                engine = "netcdf4"
            elif output_name.split(".")[-1] == "zarr" and engine is None:
                engine = "zarr"
            else:
                name_error = NameError(
                    f"Output name ({output_name}) has non-explicit or unmapped "
                    "extension please specify an engine to open it."
                )
                logging.error(name_error)
                raise name_error
            store_name = output_name.rsplit(".", maxsplit=1)[0] + ".zarr"
            dataset = xr.open_dataset(output_name, engine=engine)
        else:
            attribute_error = AttributeError(
                "Not enough inputs, specify either a filepath "
                "or pass a valid subset_request with credentials"
            )
            raise attribute_error
        return dataset, store_name

    def _open_dataset_as_out_type(
        xarray_dataset: xr.Dataset, out_type: str, store_name: str
    ):
        if out_type == "zarr":
            store = zarr.DirectoryStore(store_name)
            xarray_dataset.to_zarr(store, mode="w")
            return zarr.open(store)
        elif out_type == "xarray":
            return xarray_dataset
        elif out_type == "pandas":
            return xarray_dataset.to_dataframe()

    xarray_dataset, store_name = _open_dataset_as_xarray(
        filepath, username, password, subset_request, engine
    )
    return _open_dataset_as_out_type(xarray_dataset, out_type, store_name)
