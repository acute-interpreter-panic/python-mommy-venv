from pathlib import Path
import json
from typing import Dict, Optional, List
import os
import logging
import toml
import random
import requests

from .static import get_config_file


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



def _load_config_file(config_file: Path) -> Dict[str, List[str]]:
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
    

def compile_config(disable_requests: bool = False) -> dict:
    global RESPONSES_FILE, RESPONSES_URL

    data = json.loads(RESPONSES_FILE.read_text())
    
    if not disable_requests:
        print("mommy downloads newest responses for her girl~")
        print(RESPONSES_URL)
        print()
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
    config_file = get_config_file()
    if config_file is not None:
        config.update(_load_config_file(config_file))

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

    return compiled
