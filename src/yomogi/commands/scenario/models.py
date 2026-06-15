from dataclasses import dataclass, field
from typing import Literal

from markupsafe import Markup

RichText = str | Markup


@dataclass
class DocumentTitle:
    text: RichText
    type: Literal["title"] = field(init=False, default="title")


@dataclass
class PartTitle:
    text: RichText
    type: Literal["part_title"] = field(init=False, default="part_title")


@dataclass
class TextBlock:
    text: RichText
    type: Literal["text"] = field(init=False, default="text")


@dataclass
class StageDirection:
    text: RichText
    type: Literal["togaki"] = field(init=False, default="togaki")


@dataclass
class Conversation:
    speaker: RichText
    text: RichText
    enclosure: Literal["quote", "parenthesis"] = "quote"
    gseq: int | None = None
    type: Literal["conversation"] = field(init=False, default="conversation")

    @property
    def opening_mark(self) -> str:
        return "「" if self.enclosure == "quote" else "（"

    @property
    def closing_mark(self) -> str:
        return "」" if self.enclosure == "quote" else "）"


Block = TextBlock | StageDirection | Conversation


@dataclass
class Scene:
    text: RichText
    no: str | None
    line: int
    blocks: list[Block] = field(default_factory=list)
    no_str: str = ""
    id: str | None = None
    type: Literal["scene"] = field(init=False, default="scene")


Node = DocumentTitle | PartTitle | Scene


@dataclass(frozen=True)
class ScenarioWarning:
    code: str
    message: str
    line: int | None = None
