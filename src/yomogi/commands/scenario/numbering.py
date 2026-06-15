import re
from collections import Counter

from yomogi.commands.scenario.models import (
    Conversation,
    Node,
    ScenarioWarning,
    Scene,
)

SCENE_MAIN_WIDTH = 3
RE_SCENE_LINK = re.compile(r">>\s*(\d+(?:\.\d+)*)")


def scenes(nodes: list[Node]) -> list[Scene]:
    return [node for node in nodes if isinstance(node, Scene)]


def assign_scene_numbers(nodes: list[Node], start: int = 1) -> None:
    used_numbers = {
        scene.no
        for scene in scenes(nodes)
        if scene.no is not None
    }
    number = start

    for scene in scenes(nodes):
        if scene.no is not None:
            continue
        while str(number) in used_numbers:
            number += 1
        scene.no = str(number)
        used_numbers.add(scene.no)
        number += 1


def format_scene_number(
    number: str,
    main_width: int = SCENE_MAIN_WIDTH,
) -> tuple[str, str]:
    parts = number.split(".")
    main = f"{int(parts[0]):0{main_width}d}"
    rest = parts[1:]
    label = ".".join([main, *rest])
    anchor = "scene-" + "-".join([main, *rest])
    return label, anchor


def assign_scene_ids(
    nodes: list[Node],
    main_width: int = SCENE_MAIN_WIDTH,
) -> dict[str, list[Scene]]:
    scenes_by_number: dict[str, list[Scene]] = {}

    for scene in scenes(nodes):
        if scene.no is None:
            continue
        label, base_anchor = format_scene_number(scene.no, main_width)
        occurrences = scenes_by_number.setdefault(scene.no, [])
        occurrences.append(scene)
        scene.no_str = label
        scene.id = (
            base_anchor
            if len(occurrences) == 1
            else f"{base_anchor}--{len(occurrences)}"
        )

    return scenes_by_number


def assign_dialogue_numbers(nodes: list[Node]) -> int:
    number = 1
    for scene in scenes(nodes):
        for block in scene.blocks:
            if isinstance(block, Conversation):
                block.gseq = number
                number += 1
    return number - 1


def link_targets(nodes: list[Node]) -> dict[str, str]:
    targets: dict[str, str] = {}
    for scene in scenes(nodes):
        if scene.no is not None and scene.id is not None:
            targets.setdefault(scene.no, scene.id)
    return targets


def collect_warnings(
    nodes: list[Node],
    source_text: str,
) -> list[ScenarioWarning]:
    scene_list = scenes(nodes)
    lines_by_number: dict[str, list[int]] = {}
    for scene in scene_list:
        if scene.no is not None:
            lines_by_number.setdefault(scene.no, []).append(scene.line)

    warnings: list[ScenarioWarning] = []
    for number, lines in lines_by_number.items():
        if len(lines) > 1:
            locations = ", ".join(str(line) for line in lines)
            warnings.append(
                ScenarioWarning(
                    code="duplicate-scene-number",
                    message=f"duplicate scene number {number} (lines {locations})",
                )
            )

    duplicate_numbers = {
        number
        for number, count in Counter(
            scene.no for scene in scene_list if scene.no is not None
        ).items()
        if count > 1
    }
    for line_number, line in enumerate(source_text.splitlines(), 1):
        for match in RE_SCENE_LINK.finditer(line):
            number = match.group(1)
            if number in duplicate_numbers:
                warnings.append(
                    ScenarioWarning(
                        code="ambiguous-scene-link",
                        message=(
                            f"scene link {number} is ambiguous at line "
                            f"{line_number}; linking to first occurrence"
                        ),
                        line=line_number,
                    )
                )

    return warnings


def prepare_numbering(
    nodes: list[Node],
    source_text: str,
) -> list[ScenarioWarning]:
    assign_scene_numbers(nodes)
    assign_scene_ids(nodes)
    assign_dialogue_numbers(nodes)
    return collect_warnings(nodes, source_text)
