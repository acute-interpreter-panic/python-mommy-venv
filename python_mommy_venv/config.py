from typing import Optional, List, Dict
import os
from os.path import expandvars
from sys import platform
import logging
from pathlib import Path
import toml
import random

from .static import RESPONSES

logger = logging.Logger("mommy_config")

PREFIXES = [
    "PYTHON", # first one is always the prefix of the current program
    "CARGO",
]


# env key is just a backup key for compatibility with cargo mommy
CONFIG = {
    "mood": {
        "defaults": ["chill"]
    },
    "emote": {
        "defaults": ["❤️", "💖", "💗", "💓", "💞"]
    },
    "pronoun": {
        "defaults": ["her"]
    },
    "role": {
        "defaults": ["mommy"]
    },
    "affectionate_term": {
        "defaults": ["girl"],
        "env_key": "LITTLE"
    },
    "denigrating_term": {
        "spiciness": "yikes",
        "defaults": ["slut", "toy", "pet", "pervert", "whore"],
        "env_key": "FUCKING"
    },
    "part": {
        "spiciness": "yikes",
        "defaults": ["milk"]
    }
}

MOOD_PRIORITIES: Dict[str, int] = {}
for i, mood in enumerate(RESPONSES):
    MOOD_PRIORITIES[mood] = i

PREFIXES = [
    "PYTHON", # first one is always the prefix of the current program
    "CARGO",
]

for key, value in CONFIG.items():
    env_keys = [
        PREFIXES[0] + "_MOMMY_" + key.upper(),
        "MOMMY_" + key.upper(),
        *(p + "_MOMMY_" + key.upper() for p in PREFIXES)
    ]

    if value.get("env_key") is not None:
        env_keys.append(value.get("env_key"))

    for env_key in env_keys:
        res = os.environ.get(env_key)
        if res is not None:
            value["default"] = res.split("/")


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
    global CONFIG
    if not config_file.exists():
        return False

    with config_file.open("r") as f:
        data = toml.load(f)
        
        for key, value in data.items():
            if isinstance(value, str):
                CONFIG[key]["defaults"] = [value]
            else:
                CONFIG[key]["defaults"] = value

    return True


for c in CONFIG_FILES:
    if load_config_file(c):
        break


# validate config file
if True:
    unfiltered_moods = CONFIG["mood"]["defaults"]
    CONFIG["mood"]["defaults"] = filtered_moods = []
    for mood in unfiltered_moods:
        if mood in RESPONSES:
            filtered_moods.append(mood)
        else:
            logger.warning("mood %s isn't supported", mood)


def get_mood() -> str:
    return random.choice(CONFIG["mood"]["defaults"]) 

def get_template_values(mood: str) -> Dict[str, str]:
    mood_spice_level = MOOD_PRIORITIES[mood]
    result = {}
    
    for key, value in CONFIG.items():
        spice = value.get("spiciness")
        allow_key = spice is None
        if not allow_key:
            key_spice_level = MOOD_PRIORITIES[spice]
            allow_key = mood_spice_level >= key_spice_level
        
        if not allow_key:
            continue

        result[key] = random.choice(value["defaults"])

    return result
