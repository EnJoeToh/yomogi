from yomogi.commands.scenario.models import (
    Conversation,
    DocumentTitle,
    PartTitle,
    Scene,
    StageDirection,
    TextBlock,
)
from yomogi.commands.scenario.parser import parse_text


def test_parse_scenario_structure():
    nodes = parse_text(
        "☆ 題名\n"
        "★ 第一部\n"
        "■ 100 導入\n"
        "＠ 部屋。\n"
        "太郎「こんにちは」\n"
        "本文\n"
    )

    assert isinstance(nodes[0], DocumentTitle)
    assert isinstance(nodes[1], PartTitle)
    assert isinstance(nodes[2], Scene)
    assert nodes[2].no == "100"
    assert nodes[2].line == 3
    assert isinstance(nodes[2].blocks[0], StageDirection)
    assert isinstance(nodes[2].blocks[1], Conversation)
    assert isinstance(nodes[2].blocks[2], TextBlock)


def test_blank_line_closes_current_scene():
    nodes = parse_text("■ 100 最初\n本文\n\n■ 200 次\n本文\n")

    assert [node.no for node in nodes if isinstance(node, Scene)] == [
        "100",
        "200",
    ]


def test_parse_conversation_enclosures_and_speaker_supplement():
    nodes = parse_text(
        "■ 100 導入\n"
        "太郎（電話）「聞こえる？」\n"
        "花子（小声）（聞こえるよ）\n"
    )

    scene = nodes[0]
    assert isinstance(scene, Scene)
    quoted, parenthetical = scene.blocks
    assert isinstance(quoted, Conversation)
    assert quoted.speaker == "太郎（電話）"
    assert quoted.text == "聞こえる？"
    assert quoted.enclosure == "quote"
    assert isinstance(parenthetical, Conversation)
    assert parenthetical.speaker == "花子（小声）"
    assert parenthetical.text == "聞こえるよ"
    assert parenthetical.enclosure == "parenthesis"
