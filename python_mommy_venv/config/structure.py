from typing import TypedDict, List, Dict
from typing_extensions import NotRequired


class Config(TypedDict):
    moods:  Dict[str, Dict[str, List[str]]]
    vars:   Dict[str, List[str]]


class VarDefinition(TypedDict):
    defaults:   List[str]
    env_key:    NotRequired[str]
    spiciness:  NotRequired[str]


class Responses(TypedDict):
    etag:   str
    moods:  Dict[str, Dict[str, List[str]]]
    vars:   Dict[str, VarDefinition]


class ConfigFile(TypedDict):
    moods:  NotRequired[List[str]]
    vars:   NotRequired[Dict[str, List[str]]]
