from typing import TypedDict, List, Dict
from typing_extensions import NotRequired


class Advanced(TypedDict):
    disable_requests: bool
    print_time: bool
    print_mommy_time: bool


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
    print_mommy_time: NotRequired[bool]
    disable_requests: NotRequired[bool]


class ConfigFile(TypedDict):
    moods:      NotRequired[List[str]]
    vars:       NotRequired[Dict[str, List[str]]]
    advanced:   NotRequired[ConfigFileAdvanced]

