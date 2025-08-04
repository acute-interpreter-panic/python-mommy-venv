from __future__ import annotations

from pathlib import Path
from typing import Optional
import sys
from collections.abc import Iterator
import requests
import json
import toml

from xdg_base_dirs import xdg_config_home, xdg_cache_home


from . import structure


def _get_config_files() -> Iterator[Path]:
    file_names = ("python-mommy.toml", "mommy.toml")

    # check if mommy runs in venv
    if sys.prefix != sys.base_prefix:
        base_dir = Path(sys.prefix)
        for name in file_names:
            yield base_dir / name

    # files in working directory
    for name in file_names:
        yield Path(name)

    # files in .config directory
    base_dir = xdg_config_home() / "mommy"
    for name in file_names:
            yield base_dir / name


def _get_config_file() -> Optional[Path]:
    for possible in _get_config_files():
        if possible.exists():
            return possible
        

def load_config_file() -> Optional[structure.ConfigFile]:
    file = _get_config_file()
    if file is None:
        return None
    
    with file.open("r") as f:
        return toml.load(f)


def load_responses(disable_requests: bool = False) -> structure.Responses:
    _p: Path = xdg_cache_home() / "mommy"
    _p.mkdir(exist_ok=True)

    responses_file = _p / "responses.json"

    if not responses_file.exists():
        included_file = Path(__file__).parent.parent / "responses.json"
        responses_file.write_bytes(included_file.read_bytes())

    with responses_file.open("r") as f:
        data = json.load(f)

    responses_url = "https://raw.githubusercontent.com/Gankra/cargo-mommy/refs/heads/main/responses.json"

    fetch_new = False
    if not disable_requests:
        original_etag = data["etag"]
        res = requests.head(responses_url)
        fetch_new = original_etag != res.headers["etag"]
    if fetch_new:
        res = requests.get(responses_url)
        data = res.json()
        data["etag"] = res.headers["etag"]

        with responses_file.open("w") as f:
            json.dump(data, f, indent=4)

    return data