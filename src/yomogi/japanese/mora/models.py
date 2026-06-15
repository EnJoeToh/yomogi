from dataclasses import dataclass


@dataclass(frozen=True)
class Mora:
    text: str
    consonant: str
    vowel: str


@dataclass(frozen=True)
class MoraLine:
    source: str
    moras: tuple[Mora, ...]
