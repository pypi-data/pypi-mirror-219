import os

OVERWRITE_SHORT_OPTION = "--overwrite"
OVERWRITE_LONG_OPTION = "--overwrite-output-data"
OVERWRITE_OPTION_HELP_TEXT = (
    "If specified and if the file already exists on destination, then it will be "
    "overwritten instead of creating new one with unique index."
)

FORCE_DOWNLOAD_CLI_PROMPT_MESSAGE = "Do you want to proceed with download?"


def get_unique_filename(filepath: str) -> str:
    filename, extension = os.path.splitext(filepath)
    counter = 1

    while os.path.exists(filepath):
        filepath = filename + "_(" + str(counter) + ")" + extension
        counter += 1

    return filepath
