from collections import defaultdict
from collections.abc import Iterable
from typing import DefaultDict, List, Optional
import os
import logging
from functools import lru_cache

from . import structure
from . import utils as _u

from ..utils import MOMMY


mommy_logger = logging.getLogger("mommy")
serious_logger = logging.getLogger("serious")


def _env_names_from_key(key: str) -> Iterable[str]:
    for m in ("MOMMY", "DADDY"):
        base = m + "_" + key.upper()
        yield "PYTHON_" + base
        yield base
        yield "CARGO_" + base


def _get_env_value(env_keys: List[str]) -> Optional[List[str]]:
    for key in env_keys:
        for var in _env_names_from_key(key):
            r = os.getenv(var)
            if r is not None:
                return r.split("/")


def load_config(disable_requests: bool = False) -> structure.Config:
    config: structure.Config = {
        "moods":    {},
        "vars":     {},
        "advanced": {
            "print_time": False,
            "print_mommy_time": False,
            "disable_requests": False,
        },
    }

    config_file = _u.load_config_file()
    if config_file is not None:
        config["advanced"].update(config_file.get("advanced", {}))

    responses = _u.load_responses(disable_requests=config["advanced"]["disable_requests"])
    # mood can just be copied
    config["moods"] = responses["moods"]
    # vars actually define the config
    var_definitions = responses["vars"]
    
    # fill up with default values
    for name, definition in var_definitions.items():
        config["vars"][name] = definition["defaults"]
    
    defaults_override = {
        "pronoun": [MOMMY.PRONOUN],
        "role": [MOMMY.ROLE],
        "affectionate_term": [MOMMY.YOU]
    }
    for name, default in defaults_override.items():
        config["vars"][name] = default

    # update env_key in var_definitions for compatibility with cargo mommy
    # fill ADDITIONAL_ENV_VARS with the "env_key" values
    env_var_mapping: DefaultDict[str, List[str]] = defaultdict(list, {
        "pronoun":  ["PRONOUNS"],
        "role":     ["ROLES"],
        "emote":    ["EMOTES"],
        "mood":     ["MOODS"],
    })
    for name, definition in var_definitions.items():
        if "env_key" in definition:
            env_var_mapping[name].append(definition["env_key"])
        env_var_mapping[name].append(name.upper())

    # actually load env vars
    for name, definition in var_definitions.items():
        res = _get_env_value(env_var_mapping[name])
        if res is not None:
            config["vars"][name] = res

    # config file
    if config_file is not None:
        if "moods" in config_file:
            config["vars"]["mood"] = config_file["moods"]
        config["vars"].update(config_file.get("vars", {}))
        
    # validate
    # moods
    selected_moods = config["vars"].pop("mood")
    for mood in selected_moods:
        if mood not in config["moods"]:
            supported_moods_str = ", ".join(config["moods"].keys())
            mommy_logger.error(
                "%s doesn't know how to feel %s... %s moods are %s",
                MOMMY.ROLE,
                mood,
                MOMMY.PRONOUN,
                supported_moods_str,
            )
            serious_logger.error(
                "mood '%s' doesn't exist. moods are %s",
                mood,
                supported_moods_str,
            )
            exit(1)
    config["moods"] = {
        key: value
        for key, value in config["moods"].items()
        if key in selected_moods
    }
    # empty vars
    empty_values = []
    for key, value in config["vars"].items():
        if len(value) == 0:
            empty_values.append(key)
    if len(empty_values) > 0:
        empty_values_sting = ", ".join(empty_values)
        mommy_logger.error(
            "%s is very displeased that %s %s didn't config the key(s) %s",
            MOMMY.ROLE,
            MOMMY.PRONOUN,
            MOMMY.YOU,
            empty_values_sting,
        )
        serious_logger.error(
            "the following keys have empty values and need to be configured: %s",
            empty_values_sting
        )
        exit(1)

    return config
