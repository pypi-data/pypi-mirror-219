# Copernicus Marine Service client

A library to facilitate the access of Copernicus Marine Service products and datasets.

## Introduction

This package allows to recover products and datasets information from Command Line Interface or with Python code,
as well as download subsets and native files.

## Command Line Interface (CLI)

### Command *describe*

Retrieve information about all products as JSON:

```txt
> copernicus-marine describe
{
  "products": [
    {
      "title": "Antarctic Sea Ice Extent from Reanalysis",
      "product_id": "ANTARCTIC_OMI_SI_extent",
      "thumbnail_url": "https://catalogue.marine.copernicus.eu/documents/IMG/ANTARCTIC_OMI_SI_extent.png",
      "production_center": "Mercator Oc\u00e9an International",
      "creation_datetime": "2018-02-12",
      "modified_datetime": "2018-02-12",
    }
    ...
  ]
}
```

Retrieve all information about datasets as JSON:

```txt
> copernicus-marine describe --include-datasets
{
  "products": [
    {
      "title": "Antarctic Sea Ice Extent from Reanalysis",
      "product_id": "ANTARCTIC_OMI_SI_extent",
      "thumbnail_url": "https://catalogue.marine.copernicus.eu/documents/IMG/ANTARCTIC_OMI_SI_extent.png",
      "production_center": "Mercator Oc\u00e9an International",
      "creation_datetime": "2018-02-12",
      "modified_datetime": "2018-02-12",
      "datasets": [
        {
          "dataset_id": "antarctic_omi_si_extent",
          "dataset_name": "antarctic_omi_si_extent",
          "services": [
            {
              "protocol": "ftp",
              "uri": "ftp://my.cmems-du.eu/Core/ANTARCTIC_OMI_SI_extent/antarctic_omi_si_extent"
            }
          ],
          "variables": []
        }
      ]
    },
    ...
  ]
}
```

### Command *login*

Create the configuration files for access to the copernicus marine service:
'.dodsrc', '.netrc', '.motuclient-python.ini'.
The directory to store these configuration files can be modified by the user using the "config-file-directory" option
but beware as it should also be passed to the *subset* and *native* command afterwards.
By default, if the configuration files already exist, the user is asked for confirmation to overwrite them.

Example:
'''
> copernicus marine login
< Username :
< Password :
> INFO     - root - Configuration files stored in ${HOME}\.copernicus_marine_client
'''

### Command *subset*

Download a dataset subset, based on dataset id, variable names and attributes slices:

```txt
> copernicus-marine subset -i METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2 -v analysed_sst -v sea_ice_fraction -t 2021-01-01 - T 2021-01-03 -x 0.0 -X 0.1 -y 0.0 -Y 0.1

< Username:
< Password:
< Trying to download as one file...
```

File downloaded to ./{dataset_id}.{nc/zarr} if not specified otherwise (through -o/--output-directory and -f/--output-filename options). If the output-filename argument ends with '.nc' suffix, the file will be downloaded as a netCDF file.

### Command *native*

Download a native file (or files), based on dataset id or path to files:

Example:

```txt
> copernicus-marine native -u ftp://my.cmems-du.eu/Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/

< Username:
< Password:
< You requested the download of the following files:
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202207.nc - 3.27 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202208.nc - 3.29 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202209.nc - 3.28 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202210.nc - 3.26 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202211.nc - 3.26 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202212.nc - 3.26 MB

Total size of the download: 19.62 MB


Do you want to proceed with download? [y/N]:
```

File(s) downloaded to ./{path}/{filename} if not specified otherwise:

- "--output-path" specifies a directory to dump the files in
- "--no-directories" to not recreate the folder structure

If not specified otherwise, after the header display with a summary of the request,
the user is asked for confirmation:

- "--no-confirmation" to turn down the confirmation prompt
- "--show-outputnames" to display the full paths of the outputs files

Option `--filter TEXT` allows to specify a Unix shell-style wildcard pattern (see [fnmatch — Unix filename pattern matching](https://docs.python.org/3/library/fnmatch.html)) and select specific files. It work with both `--dataset-id` and `--dataset-url` options.

Option `--regex TEXT` allows to specify a regular expression and select specific files. It work with both `--dataset-id` and `--dataset-url` options.

Example:
```
> copernicus-marine native -u ftp://my.cmems-du.eu/Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m --regex ".*2022(08|09|10).nc"
Password:
You requested the download of the following files:
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202208.nc - 3.29 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202209.nc - 3.28 MB
Core/NWSHELF_MULTIYEAR_BGC_004_011/cmems_mod_nws_bgc-pft_myint_7km-3D-diato_P1M-m/2022/metoffice_foam1_amm7_NWS_DIATO_CPWC_mm202210.nc - 3.26 MB

Total size of the download: 9.82 MB


Do you want to proceed with download? [y/N]:
```

### The overwrite option

Both `native` and `subset` commands provide an `--overwrite-ouput-data` option.
When not provided (default behavior), once the download has been accepted (or if the `--force-download` option was provided), if the file already exists on destination, then a new one with a unique index will be created.
On the other hand, if the `--overwrite-ouput-data` option is provided and the file already exists, then it'll be overwritten.

### The `--help` argument

In any case, please remember that you can call the `--help` argument on any CLI option. This may save you some time or find what you need.

## Python functions

The library also provide python functions to help with catalogue
browsing and datasets download in scripts.

### Basic example

In this example 4 steps are performed:
  1- Fetch the catalogue to select a dataset
  2- Construct a SubsetRequest for this dataset
  3- Download the subset as a zarr store
  4- Open the subset as an xarray dataset

```python
import copernicus_marine_client as cmc

# Step 1: Fetch catalogue and parse information on dataset
catalogue = cmc.fetch_catalogue()
dataset_id = "cmems_mod_ibi_bgc_anfc_0.027deg-3D_P1D-m"
assert dataset_id in cmc.get_all_dataset_ids()
dataset = catalogue.filter([dataset_id]).products[0].datasets[0]
# Object "dataset" can be used to display all the metadata necessary to build a SubsetRequest
variable = [
    variable for variable in dataset.variables if variable.short_name in ["zooc"]
][0]
coordinates = {
    coordinate.coordinates_id: (coordinate.minimum_value, coordinate.maximum_value)
    for coordinate in variable.coordinates
}

# Step 2: Construct the request based on parsed information
subset_request = cmc.SubsetRequest(
    dataset_id="cmems_mod_ibi_bgc_anfc_0.027deg-3D_P1D-m",
    start_datetime="2023-04-20",
    end_datetime="2023-04-21",
    minimal_latitude=30.0,
    maximal_latitude=30.1,
    minimal_longitude=0.1,
    maximal_longitude=0.2,
    minimal_depth=100,
    maximal_depth=1000,
    variables=["zooc"],
    force_protocol="zarr-map",
    output_directory="data_folder",
    output_filename="datastore.zarr",
    force_download=True,
)

# Step 3: Download the subset based on request content
filename = cmc.download_subset(
    login="FAKE_LOGIN", password="FAKE_PASSWORD", subset_request=subset_request
)

# Step 4: Open the downloaded subset as an xarray dataset
subset = cmc.open_dataset(filepath=filename, engine="zarr", out_type="xarray")
```

## Installation

Using pip, for example:

```shell
pip install copernicus-marine-client
```

## Technical details

This module is organized around two capabilities:

- a catalogue, parsed from web requests, that contains informations on the available datasets
- a downloader, to simplify the download of dataset files or subsets

The catalogue can be displayed by the user and is used by the downloader to link the user
requests with files or subset of files to retrieve.
The downloader will help the user download the needed datasets.

A rigid format, specified in "request_structure.py" is used to ensure conformity of the information passed between the CLI command and the python functions.

For subset command, the format is:

```python
@dataclass
class SubsetRequest:
    dataset_url: Optional[str] = None
    dataset_id: Optional[str] = None
    variables: Optional[List[str]] = None
    minimal_longitude: Optional[float] = None
    maximal_longitude: Optional[float] = None
    minimal_latitude: Optional[float] = None
    maximal_latitude: Optional[float] = None
    minimal_depth: Optional[float] = None
    maximal_depth: Optional[float] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    output_directory: Optional[str] = None
    output_filename: Optional[str] = None
    force_download: Optional[bool] = None
    force_protocol: Optional[str] = None
```
