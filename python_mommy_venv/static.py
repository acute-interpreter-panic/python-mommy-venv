from __future__ import annotations

from pathlib import Path
import os
import logging
from typing import Optional
import sys


logger = logging.Logger(__name__)


class MOMMY:
    ROLE = "mommy"
    PRONOUN = "her"

    @classmethod
    def set_roles(cls, is_mommy: bool):
        if is_mommy:
            cls.ROLE = "mommy"
            cls.PRONOUN = "her"
        else:
            cls.ROLE = "daddy"
            cls.PRONOUN = "his"


def set_mommy_roles(is_mommy: bool):
    global MOMMY_NAME, MOMMY_PRONOUN
    print(is_mommy)

    if is_mommy:
        MOMMY_NAME = "mommy"
        MOMMY_PRONOUN = "her"
    else:
        MOMMY_NAME = "daddy"
        MOMMY_PRONOUN = "his"

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


def _get_xdg_config_dir() -> Path:
    res = os.environ.get("XDG_CONFIG_HOME")
    if res is not None:
        return Path(res)

    xdg_user_dirs_file = Path(os.environ.get("XDG_CONFIG_HOME") or Path(Path.home(), ".config", "user-dirs.dirs"))
    xdg_user_dirs_default_file = Path("/etc/xdg/user-dirs.defaults")

    def get_dir_from_xdg_file(xdg_file_path: Path, key_a: str) -> Optional[str]:
        if not xdg_file_path.exists():
            logger.info("config file not found in %s", str(xdg_file_path))
            return

        with xdg_file_path.open("r") as f:
            for line in f:
                if line.startswith("#"):
                    continue

                parts = line.split("=")
                if len(parts) > 2:
                    continue

                key_b = parts[0].lower().strip()
                value = parts[1].strip().split("#")[0]

                if key_a.lower() == key_b:
                    return value

        logger.info("key %s not found in %s", key_a, str(xdg_file_path))

    res = get_dir_from_xdg_file(xdg_user_dirs_file, "XDG_CONFIG_HOME")
    if res is not None:
        return Path(res)

    res = get_dir_from_xdg_file(xdg_user_dirs_default_file, "CONFIG")
    if res is not None:
        return Path(Path.home(), res)


    res = get_dir_from_xdg_file(xdg_user_dirs_default_file, "XDG_CONFIG_HOME")
    if res is not None:
        return Path(Path.home(), res)

    default = Path(Path.home(), ".config")
    logging.info("falling back to %s", default)
    return default


CONFIG_DIRECTORY = _get_xdg_config_dir() / "mommy"
COMPILED_CONFIG_FILE_NAME = "compiled-mommy.json"

IS_VENV = sys.prefix != sys.base_prefix
VENV_DIRECTORY = Path(sys.prefix)

def get_config_file() -> Optional[Path]:
    config_files = []
    if IS_VENV:
        config_files.extend([
            VENV_DIRECTORY / "python-mommy.toml",
            VENV_DIRECTORY / "mommy.toml",
        ])
    config_files.extend([
        CONFIG_DIRECTORY / "python-mommy.toml",
        CONFIG_DIRECTORY / "mommy.toml",
    ])

    for f in config_files:
        if f.exists():
            return f


def get_compiled_config_file() -> Path:
    compiled_config_files = [
        VENV_DIRECTORY / "compiled-mommy.json",
        CONFIG_DIRECTORY / "compiled-mommy.json",
    ]

    for f in compiled_config_files:
        if f.exists():
            return f
        
    raise Exception("couldn't find compiled config file")
