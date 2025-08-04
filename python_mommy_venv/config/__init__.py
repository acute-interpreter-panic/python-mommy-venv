from collections import defaultdict
from collections.abc import Iterable
from typing import DefaultDict, List, Optional
import os
import logging

from . import structure
from . import utils as _u

from ..static import MOMMY


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
    }

    responses = _u.load_responses(disable_requests=disable_requests)
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
                

    return config
