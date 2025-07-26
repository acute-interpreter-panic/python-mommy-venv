from typing import Optional, List
import os
import logging
from pathlib import Path

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
