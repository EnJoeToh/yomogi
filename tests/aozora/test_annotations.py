from yomogi.commands.aozora.annotations import replace_annotation


def test_fullwidth_indent_becomes_ideographic_spaces():
    assert replace_annotation("３字下げ") == "　　　"


def test_middle_heading_annotation_is_removed():
    assert replace_annotation("「第一章」は中見出し") == ""


def test_large_heading_annotation_is_removed():
    assert replace_annotation("「第一部」は大見出し") == ""


def test_exact_gaiji_annotation_is_replaced():
    assert replace_annotation("「目＋爭」、第3水準1-88-85") == "睜"


def test_gaiji_source_locations_are_ignored():
    assert replace_annotation("「口＋堯」、U+5635、71-2") == "嘵"
    assert replace_annotation("「口＋堯」、U+5635、112-13") == "嘵"
    assert replace_annotation("濁点付き小書き平仮名つ、25-10") == "っ゙"
    assert replace_annotation("濁点付き小書き平仮名つ、218-1") == "っ゙"


def test_unknown_annotation_has_no_replacement():
    assert replace_annotation("未対応") is None
