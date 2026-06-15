import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Literal

from sudachipy import Dictionary, SplitMode

DiffTag = Literal["equal", "delete", "insert", "replace"]

_WHITESPACE_PATTERN = re.compile(r"(\s+)")
_TOKENIZER = Dictionary(dict="core").create()


@dataclass(frozen=True)
class DiffChunk:
    tag: DiffTag
    old_text: str
    new_text: str


def tokenize(text: str) -> list[str]:
    """Tokenize Japanese text while preserving whitespace exactly."""
    tokens: list[str] = []
    for part in _WHITESPACE_PATTERN.split(text):
        if not part:
            continue
        if part.isspace():
            tokens.append(part)
            continue
        tokens.extend(
            morpheme.surface()
            for morpheme in _TOKENIZER.tokenize(part, SplitMode.A)
        )
    return tokens


def compare(old_text: str, new_text: str) -> list[DiffChunk]:
    old_tokens = tokenize(old_text)
    new_tokens = tokenize(new_text)
    matcher = SequenceMatcher(a=old_tokens, b=new_tokens, autojunk=False)

    chunks: list[DiffChunk] = []
    for tag, old_start, old_end, new_start, new_end in matcher.get_opcodes():
        chunks.append(
            DiffChunk(
                tag=tag,
                old_text="".join(old_tokens[old_start:old_end]),
                new_text="".join(new_tokens[new_start:new_end]),
            )
        )
    return chunks
