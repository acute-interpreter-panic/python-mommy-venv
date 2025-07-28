from pathlib import Path
import json
from typing import Dict, Optional, List
import os
import logging
import toml
import random
import requests


logger = logging.Logger(__name__)
PREFIX = "MOMMY"

RESPONSES_URL = "https://raw.githubusercontent.com/diamondburned/go-mommy/refs/heads/main/responses.json"
RESPONSES_FILE = Path(__file__).parent / "responses.json"
ADDITIONAL_ENV_VARS = {
    "pronoun": "PRONOUNS",
    "role": "ROLES",
    "emote": "EMOTES",
    "mood": "MOODS",
}

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
CONFIG_FILES = [
    CONFIG_DIRECTORY / "python-mommy.toml",
    CONFIG_DIRECTORY / "mommy.toml",
]
COMPILED_CONFIG_FILE = CONFIG_DIRECTORY / "responses.json"

def _load_config_file(config_file: Path) -> Optional[Dict[str, List[str]]]:
    global CONFIG
    if not config_file.exists():
        return None

    with config_file.open("r") as f:
        data = toml.load(f)
        
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = [value]
            else:
                result[key] = value

        return result


ADDITIONAL_PROGRAM_PREFIXES = [
    "cargo",    # only as fallback if user already configured cargo
]

def _get_env_var_names(name: str): 
    BASE = PREFIX + "_" + name.upper()
    yield "PYTHON_" + BASE
    yield BASE
    for a in ADDITIONAL_PROGRAM_PREFIXES:
        yield a + "_" + BASE

def _get_env_value(name: str) -> Optional[str]:
    if name in ADDITIONAL_ENV_VARS:
        for key in _get_env_var_names(ADDITIONAL_ENV_VARS[name]):
            val = os.environ.get(key)
            if val is not None:
                return val
    
    for key in _get_env_var_names(name):
        val = os.environ.get(key)
        if val is not None:
            return val
    

def compile_config(disable_requests: bool = False):
    global RESPONSES_FILE, RESPONSES_URL

    data = json.loads(RESPONSES_FILE.read_text())
    
    if not disable_requests:
        print("mommy downloads newest responses for her girl~")
        print(RESPONSES_URL)
        r = requests.get(RESPONSES_URL)
        data = r.json()

    config_definition: Dict[str, dict] = data["vars"]
    mood_definitions: Dict[str, dict] = data["moods"]

    # environment variables for compatibility with cargo mommy
    # fill ADDITIONAL_ENV_VARS with the "env_key" values
    for key, conf in config_definition.items():
        if "env_key" in conf:
            ADDITIONAL_ENV_VARS[key] = conf["env_key"]

    # set config to the default values
    config: Dict[str, List[str]] = {}
    for key, conf in config_definition.items():
        config[key] = conf["defaults"]

    # load config file
    config_file_data: Optional[Dict[str, List[str]]]
    for c in CONFIG_FILES:
        config_file_data = _load_config_file(c)
        if config_file_data is not None:
            break
    
    if config_file_data is not None:
        config.update(config_file_data)
    

    # fill config with env
    for key, conf in config_definition.items():
        val = _get_env_value(key)
        if val is not None:
            config[key] = val.split("/")

    # validate moods
    for mood in config["mood"]:
        if mood not in mood_definitions:
            supported_moods_str = ", ".join(mood_definitions.keys())
            print(f"{random.choice(config['role'])} doesn't know how to feel {mood}... {random.choice(config['pronoun'])} moods are {supported_moods_str}")
            exit(1)

    # compile
    compiled = {}
    compiled_moods = compiled["moods"] = {}
    compiled_vars = compiled["vars"] = {}

    for mood in config["mood"]:
        compiled_moods[mood] = mood_definitions[mood]
    del config["mood"]
    compiled_vars.update(config)

    print("writing compiled config to " + str(COMPILED_CONFIG_FILE))
    with COMPILED_CONFIG_FILE.open("w") as f:
        json.dump(compiled, f, indent=4)
