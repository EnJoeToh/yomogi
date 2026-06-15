from yomogi.commands.scenario.models import Conversation, Scene
from yomogi.commands.scenario.numbering import (
    assign_dialogue_numbers,
    assign_scene_ids,
    assign_scene_numbers,
    collect_warnings,
    link_targets,
)


def test_scene_numbers_are_identifiers_and_keep_file_order():
    nodes = [
        Scene(text="現在", no="200", line=1),
        Scene(text="過去", no="100", line=2),
    ]

    assign_scene_numbers(nodes)
    assign_scene_ids(nodes)

    assert [scene.no for scene in nodes] == ["200", "100"]
    assert [scene.id for scene in nodes] == ["scene-200", "scene-100"]


def test_unnumbered_scenes_use_unused_numbers():
    nodes = [
        Scene(text="明示", no="1", line=1),
        Scene(text="自動", no=None, line=2),
    ]

    assign_scene_numbers(nodes)

    assert [scene.no for scene in nodes] == ["1", "2"]


def test_duplicate_numbers_get_unique_ids_and_warnings():
    nodes = [
        Scene(text="最初", no="100", line=1),
        Scene(text="二番目", no="100", line=4),
    ]
    assign_scene_ids(nodes)

    warnings = collect_warnings(nodes, "■ 100 最初\n本文\n\n■ 100 二番目\n>> 100\n")

    assert [scene.id for scene in nodes] == ["scene-100", "scene-100--2"]
    assert link_targets(nodes) == {"100": "scene-100"}
    assert [warning.code for warning in warnings] == [
        "duplicate-scene-number",
        "ambiguous-scene-link",
    ]
    assert "lines 1, 4" in warnings[0].message
    assert "line 5" in warnings[1].message


def test_dialogue_numbers_are_global_and_sequential():
    first = Conversation("太郎", "一つ目")
    second = Conversation("花子", "二つ目")
    nodes = [
        Scene(text="一", no="100", line=1, blocks=[first]),
        Scene(text="二", no="200", line=3, blocks=[second]),
    ]

    assert assign_dialogue_numbers(nodes) == 2
    assert [first.gseq, second.gseq] == [1, 2]
