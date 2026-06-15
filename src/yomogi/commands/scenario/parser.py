import re

from yomogi.commands.scenario.models import (
    Conversation,
    DocumentTitle,
    Node,
    PartTitle,
    Scene,
    StageDirection,
    TextBlock,
)

RE_DOC_TITLE = re.compile(r"^☆\s*(.+)\s*$")
RE_PART_TITLE = re.compile(r"^★\s*(.+)\s*$")
RE_SCENE = re.compile(r"^■\s*(?:(\d+(?:\.\d+)*)\s+)?(.+?)\s*$")
RE_TOGAKI = re.compile(r"^＠\s*(.+)\s*$")
RE_QUOTED_CONVERSATION = re.compile(r"^\s*(.+?)\s*「(.*)」\s*$")
RE_PARENTHETICAL_CONVERSATION = re.compile(r"^\s*(.+)\s*（(.*)）\s*$")


def parse_text(text: str) -> list[Node]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return parse_lines(normalized.splitlines())


def parse_lines(lines: list[str]) -> list[Node]:
    nodes: list[Node] = []
    current_scene: Scene | None = None

    def close_scene() -> None:
        nonlocal current_scene
        if current_scene is not None:
            nodes.append(current_scene)
        current_scene = None

    def ensure_scene(line_number: int) -> Scene:
        nonlocal current_scene
        if current_scene is None:
            current_scene = Scene(text="", no=None, line=line_number)
        return current_scene

    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            close_scene()
            continue

        if match := RE_DOC_TITLE.match(line):
            close_scene()
            nodes.append(DocumentTitle(match.group(1).strip()))
            continue

        if match := RE_PART_TITLE.match(line):
            close_scene()
            nodes.append(PartTitle(match.group(1).strip()))
            continue

        if match := RE_SCENE.match(line):
            close_scene()
            current_scene = Scene(
                no=match.group(1),
                text=match.group(2).strip(),
                line=line_number,
            )
            continue

        if match := RE_TOGAKI.match(line):
            ensure_scene(line_number).blocks.append(
                StageDirection(match.group(1).strip())
            )
            continue

        if match := RE_QUOTED_CONVERSATION.match(line):
            ensure_scene(line_number).blocks.append(
                Conversation(
                    speaker=match.group(1).strip(),
                    text=match.group(2).strip(),
                    enclosure="quote",
                )
            )
            continue

        if match := RE_PARENTHETICAL_CONVERSATION.match(line):
            ensure_scene(line_number).blocks.append(
                Conversation(
                    speaker=match.group(1).strip(),
                    text=match.group(2).strip(),
                    enclosure="parenthesis",
                )
            )
            continue

        ensure_scene(line_number).blocks.append(TextBlock(line))

    close_scene()
    return nodes
