import re
from dataclasses import dataclass

from yomogi.commands.aozora.annotations import replace_annotation


RUBY_PATTERN = re.compile(r"《[^》]*》")
ANNOTATION_PATTERN = re.compile(r"［＃(?P<content>.*?)］")


@dataclass(frozen=True)
class NotationResult:
    text: str
    unsupported_annotations: tuple[str, ...]


def remove_ruby(text: str) -> str:
    return RUBY_PATTERN.sub("", text).replace("｜", "").replace("|", "")


def convert_notation(text: str) -> NotationResult:
    unsupported: list[str] = []

    def replace(match: re.Match[str]) -> str:
        content = match.group("content")
        replacement = replace_annotation(content)
        if replacement is None:
            unsupported.append(match.group(0))
            return match.group(0)
        return replacement

    converted = ANNOTATION_PATTERN.sub(replace, remove_ruby(text))
    return NotationResult(
        text=converted,
        unsupported_annotations=tuple(dict.fromkeys(unsupported)),
    )
