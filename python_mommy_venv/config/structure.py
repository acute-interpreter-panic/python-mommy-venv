from typing import TypedDict, List, Dict
from typing_extensions import NotRequired


class Advanced(TypedDict):
    print_time: bool


class Config(TypedDict):
    moods:      Dict[str, Dict[str, List[str]]]
    vars:       Dict[str, List[str]]
    advanced:   Advanced


class VarDefinition(TypedDict):
    defaults:   List[str]
    env_key:    NotRequired[str]
    spiciness:  NotRequired[str]


class Responses(TypedDict):
    etag:   str
    moods:  Dict[str, Dict[str, List[str]]]
    vars:   Dict[str, VarDefinition]


class ConfigFileAdvanced(TypedDict):
    print_time: NotRequired[bool]


class ConfigFile(TypedDict):
    moods:      NotRequired[List[str]]
    vars:       NotRequired[Dict[str, List[str]]]
    advanced:   NotRequired[ConfigFileAdvanced]

