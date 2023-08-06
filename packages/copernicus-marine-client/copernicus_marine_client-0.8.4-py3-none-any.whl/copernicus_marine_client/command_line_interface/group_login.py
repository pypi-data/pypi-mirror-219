import logging
import logging.config
import os
from typing import Literal, Optional, Tuple

import click

from copernicus_marine_client.configuration_files_creator import (
    check_copernicus_marine_credentials,
)
from copernicus_marine_client.configuration_files_creator import (
    main as configuration_files_creator,
)
from copernicus_marine_client.configuration_files_creator import (
    retrieve_credential_from_config_files,
)


@click.group()
def cli_group_login() -> None:
    pass


@cli_group_login.command(
    "login",
    help="""
    This command check the copernicus-marine credentials provided by the user
    and creates a configuration file with the encoded credentials if the check is valid.
    It then stores the configuration file in a directory that can be specified by
    the user.
    If the user specified a different 'config_file_directory' from default one
    ($HOME/.copernicus_marine_client), it needs to be passed also to the download
    commands.

    Examples:

    Case 1 (Recommended):

    With environment variables COPERNICUS_MARINE_SERVICE_USERNAME &
    COPERNICUS_MARINE_SERVICE_PASSWORD specified:

    > copernicus-marine login

    Case 2:

    > copernicus-marine login \n
    < Username: [USER-INPUT] \n
    < Password: [USER-INPUT]

    Case 3:

    > copernicus-marine login --username JOHN_DOE --password SECRETPASSWORD

    Case 4: Specific directory for config_files

    > copernicus-marine login --config-file-directory USER/SPECIFIED/PATH
        """,
)
@click.option(
    "--username",
    prompt="username",
    envvar="COPERNICUS_MARINE_SERVICE_USERNAME",
    hide_input=False,
    help="If not set, search for environment variable"
    + " COPERNICUS_MARINE_SERVICE_USERNAME"
    + ", or else ask for user input",
)
@click.option(
    "--password",
    prompt="password",
    envvar="COPERNICUS_MARINE_SERVICE_PASSWORD",
    hide_input=True,
    help="If not set, search for environment variable"
    + " COPERNICUS_MARINE_SERVICE_PASSWORD"
    + ", or else ask for user input",
)
@click.option(
    "--config-file-directory",
    type=str,
    default=os.path.join(os.path.expanduser("~"), ".copernicus_marine_client"),
    help="Path to the directory where the configuration file is stored",
)
@click.option(
    "--assume-yes",
    is_flag=True,
    default=False,
    help="Flag to skip confirmation before overwriting configuration file",
)
@click.option(
    "--verbose",
    type=click.Choice(["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL", "QUIET"]),
    default="INFO",
    help=(
        "Set the details printed to console by the command "
        "(based on standard logging library)."
    ),
)
def login(
    username: str,
    password: str,
    config_file_directory: str,
    force_download: bool,
    verbose: str = "INFO",
) -> None:
    if verbose == "QUIET":
        logging.root.disabled = True
        logging.root.setLevel(level="CRITICAL")
    else:
        logging.root.setLevel(level=verbose)
    check_copernicus_marine_credentials(username, password)
    configuration_files_creator(
        username=username,
        password=password,
        config_file_directory=config_file_directory,
        force_download=force_download,
    )
    logging.info(f"Configuration files stored in {config_file_directory}")


def get_credential(
    credential: Optional[str],
    credential_type: Literal["username", "password"],
    hide_input: bool,
    config_file_directory: str,
) -> str:
    if not credential:
        credential = retrieve_credential_from_config_files(
            credential_type=credential_type,
            config_file_directory=config_file_directory,
            host="my.cmems_du.eu",  # Same credentials for all hosts
        )
        if not credential:
            credential = click.prompt(credential_type, hide_input=hide_input)
            if not credential:
                raise ValueError(f"{credential} cannot be None")
    else:
        logging.debug(
            "Credentials loaded from function arguments or environment variable"
        )
    return credential


def get_username_password(
    username: Optional[str],
    password: Optional[str],
    config_file_directory: str,
) -> Tuple[str, str]:
    username = get_credential(
        username,
        "username",
        hide_input=False,
        config_file_directory=config_file_directory,
    )
    password = get_credential(
        password,
        "password",
        hide_input=True,
        config_file_directory=config_file_directory,
    )
    result_check = check_copernicus_marine_credentials(username, password)
    if result_check:
        logging.warning(
            "Invalid credentials, your download will not be authenticated"
        )
    return (username, password)


if __name__ == "__main__":
    cli_group_login()
