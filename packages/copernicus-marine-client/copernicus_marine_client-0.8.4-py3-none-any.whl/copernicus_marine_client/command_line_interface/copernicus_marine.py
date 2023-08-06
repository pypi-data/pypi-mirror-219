import json
import logging
import logging.config
import os

import click

from copernicus_marine_client.command_line_interface.group_describe import (
    cli_group_describe,
)
from copernicus_marine_client.command_line_interface.group_login import (
    cli_group_login,
)
from copernicus_marine_client.command_line_interface.group_native import (
    cli_group_native,
)
from copernicus_marine_client.command_line_interface.group_subset import (
    cli_group_subset,
)

log_config_dict = json.load(
    open(os.path.join(os.path.dirname(__file__), "..", "logging_conf.json"))
)
logging.config.dictConfig(log_config_dict)


@click.command(
    cls=click.CommandCollection,
    sources=[
        cli_group_describe,
        cli_group_login,
        cli_group_subset,
        cli_group_native,
    ],
)
@click.version_option(
    None, "-V", "--version", package_name="copernicus-marine-client"
)
def command_line_interface():
    pass


if __name__ == "__main__":
    command_line_interface()
