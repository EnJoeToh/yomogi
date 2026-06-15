import json
from importlib.resources import files
from typing import TypedDict


class MoraMapping(TypedDict, total=False):
    C: str
    V: str
    is_vowel: bool


MoraMap = dict[str, MoraMapping]


def load_mora_map() -> MoraMap:
    resource = files("yomogi.japanese.mora").joinpath("data/cv_map.json")
    with resource.open(encoding="utf-8") as source:
        return json.load(source)
