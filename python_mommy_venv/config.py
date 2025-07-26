from typing import Optional, List
import os
from os.path import expandvars
from sys import platform
import logging
from pathlib import Path
import configparser
import toml

from .static import RESPONSES

logger = logging.Logger("mommy_config")

PREFIXES = [
    "PYTHON", # first one is always the prefix of the current program
    "CARGO",
]

def _get_var(key: str, fallback: str) -> List[str]:
    value = os.environ.get(
        PREFIXES[0] + "_" + key,
        os.environ.get(
            key,
            None
        )
    )

    if value is None:
        for prefix in PREFIXES[1:]:
            value = os.environ.get(prefix + "_" + key, None)
            if value != None:
                break

    return (value or fallback).split("/")


_DEFAULT_CONFIG = {key: _get_var(key, value) for key, value in {
    "MOMMYS_ROLE": "mommy",
    "MOMMYS_PRONOUNS": "her",
    "MOMMYS_LITTLE": "girl",
    "MOMMYS_EMOTES": "❤️/💖/💗/💓/💞",
    "MOMMYS_PARTS": "milk",
    "MOMMYS_FUCKING": "slut/toy/pet/pervert/whore",
    # needs validation
    "MOMMYS_MOODS": "chill",
}.items()}

CONFIG = {}

def load_config(data: Optional[dict] = None):
    global CONFIG
    data = data if data is not None else {}

    data = {
        **_DEFAULT_CONFIG,
        **data,
    }

    # convert toml keys from snake_case to UPPER_CASE
    data = {
        key.upper(): value
        for key, value in data.items()
    }

    # validate needed values
    unfiltered_moods = data["MOMMYS_MOODS"]
    data["MOMMYS_MOODS"] = filtered_moods = []
    for mood in unfiltered_moods:
        if mood in RESPONSES:
            filtered_moods.append(mood)
        else:
            logger.warning("mood %s isn't supported", mood)

    CONFIG = data

load_config()

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


_CONFIG_DIRECTORY = _get_xdg_config_dir() / "mommy"
CONFIG_FILES = [
    _CONFIG_DIRECTORY / "python-mommy.toml",
    _CONFIG_DIRECTORY / "mommy.toml",
]

def load_config_file(config_file: Path) -> bool:
    if not config_file.exists():
        return False

    with config_file.open("r") as f:
        data = toml.load(f)
        load_config(data=data)

    return True


for c in CONFIG_FILES:
    if load_config_file(c):
        break
