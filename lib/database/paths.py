from os import path
from pathlib import Path

from lib.errors.database import PlatformNotSupportedError

import platform


def get_data_dir():
    if platform.system() == "Windows":
        return __create_data_dir(r"%APPDATA%\dsf-wegbot\db")
    elif platform.system() == "Linux":
        return __create_data_dir(r"${HOME}/.dsf-wegbot/db")
    else:
        raise PlatformNotSupportedError(platform.system())


def __create_data_dir(pathname: str):
    result = Path(path.expandvars(pathname)).resolve()
    result.mkdir(parents=True, exist_ok=True)
    return result
