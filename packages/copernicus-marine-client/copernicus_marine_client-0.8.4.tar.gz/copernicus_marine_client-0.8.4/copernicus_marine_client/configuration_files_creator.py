import base64
import configparser
import logging
import os
from netrc import netrc
from typing import Literal, Optional

import click
import lxml.html
import requests


def load_credential_from_copernicus_marine_config_file(
    credential_type: Literal["username", "password"],
    config_filename: str,
) -> Optional[str]:
    config_file = open(config_filename)
    config_string = base64.standard_b64decode(config_file.read()).decode(
        "utf8"
    )
    config = configparser.RawConfigParser()
    config.read_string(config_string)
    credential = config.get("credentials", credential_type)
    if credential:
        logging.debug(f"{credential_type} loaded from {config_filename}")
    return credential


def load_credential_from_netrc_config_file(
    credential_type: Literal["username", "password"],
    config_filename: str,
    host: str,
) -> Optional[str]:
    authenticator = netrc(config_filename).authenticators(host=host)
    if authenticator:
        username, _, password = authenticator
        logging.debug(f"{credential_type} loaded from {config_filename}")
        return username if credential_type == "username" else password
    else:
        return None


def load_credential_from_motu_config_file(
    credential_type: Literal["username", "password"],
    config_filename: str,
) -> Optional[str]:
    motu_file = open(config_filename)
    motu_credential_type = "user" if credential_type == "username" else "pwd"
    config = configparser.RawConfigParser()
    config.read_string(motu_file.read())
    credential = config.get("Main", motu_credential_type)
    if credential:
        logging.debug(f"{credential_type} loaded from {config_filename}")
    return credential


def retrieve_credential_from_config_files(
    credential_type: Literal["username", "password"],
    config_file_directory: str,
    host: str = "default_host",
) -> Optional[str]:

    copernicus_marine_client_config_filename = os.path.join(
        config_file_directory, ".copernicus_marine_client_credentials"
    )
    netrc_type = "_netrc" if os.system == "win32" else ".netrc"
    netrc_filename = os.path.join(config_file_directory, netrc_type)
    motu_filename = os.path.join(
        config_file_directory, ".motuclient-python.ini"
    )
    if os.path.exists(copernicus_marine_client_config_filename):
        credential = load_credential_from_copernicus_marine_config_file(
            credential_type, copernicus_marine_client_config_filename
        )

    elif os.path.exists(netrc_filename):
        credential = load_credential_from_netrc_config_file(
            credential_type, netrc_filename, host=host
        )
    elif os.path.exists(motu_filename):
        credential = load_credential_from_motu_config_file(
            credential_type, motu_filename
        )
    else:
        credential = None
    return credential


def create_copernicus_marine_client_config_file(
    username: str,
    password: str,
    config_file_directory: str,
    force_download: bool,
) -> None:
    config_lines = [
        "[credentials]\n",
        f"username={username}\n",
        f"password={password}\n",
    ]
    config_filename = os.path.join(
        config_file_directory, ".copernicus_marine_client_credentials"
    )
    if os.path.exists(config_filename) and not force_download:
        click.confirm(
            f"File {config_filename} already exists, overwrite it ?",
            abort=True,
        )
    config_file = open(config_filename, "w")
    config_string = base64.b64encode(
        "".join(config_lines).encode("ascii", "strict")
    ).decode("utf8")
    config_file.write(config_string)
    config_file.close()


def check_copernicus_marine_credentials(
    username: Optional[str], password: Optional[str]
) -> Optional[ConnectionRefusedError]:
    """
    Check provided Copernicus Marine Credentials are correct.

    Parameters
    ----------
    username : str
        Copernicus Marine Username, provided for free from https://marine.copernicus.eu
    password : str
        Copernicus Marine Password, provided for free from https://marine.copernicus.eu

    """
    cmems_cas_url = "https://cmems-cas.cls.fr/cas/login"
    conn_session = requests.session()
    login_session = conn_session.get(cmems_cas_url)
    login_from_html = lxml.html.fromstring(login_session.text)
    hidden_elements_from_html = login_from_html.xpath(
        '//form//input[@type="hidden"]'
    )
    playload = {
        he.attrib["name"]: he.attrib["value"]
        for he in hidden_elements_from_html
    }
    playload["username"] = username
    playload["password"] = password
    response = conn_session.post(cmems_cas_url, data=playload)
    if response.text.find("success") == -1:
        credential_error_message = ConnectionRefusedError(
            "Incorrect username or password.\n"
            "Learn how to recover your credentials at: "
            "https://help.marine.copernicus.eu/en/articles/"
            "4444552-i-forgot-my-username-or-my-password-what-should-i-do"
        )
        logging.error(credential_error_message)
        return credential_error_message
    return None


def main(
    username: str,
    password: str,
    config_file_directory: str,
    force_download: bool,
) -> None:
    if not os.path.exists(config_file_directory):
        os.makedirs(config_file_directory)
    create_copernicus_marine_client_config_file(
        username=username,
        password=password,
        config_file_directory=config_file_directory,
        force_download=force_download,
    )
