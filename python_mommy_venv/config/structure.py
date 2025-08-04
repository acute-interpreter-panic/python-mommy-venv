from typing import TypedDict, List, Dict, NotRequired


class Config(TypedDict):
    moods:  Dict[str, Dict[str, List[str]]]
    vars:   Dict[str, List[str]]


class VarDefinition(TypedDict):
    defaults: List[str]
    env_key: NotRequired[str]
    spiciness: NotRequired[str]


class Responses(TypedDict):
    etag: str
    moods: Dict[str, Dict[str, List[str]]]
    vars: Dict[str, VarDefinition]
