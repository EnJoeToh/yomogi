from yomogi.commands.diff.differ import DiffChunk, compare, tokenize
from yomogi.commands.diff.renderer import render_html


def test_tokenize_uses_sudachi_and_preserves_whitespace():
    assert tokenize("選挙管理委員会 です\n") == [
        "選挙",
        "管理",
        "委員",
        "会",
        " ",
        "です",
        "\n",
    ]


def test_compare_returns_structured_chunks():
    assert compare("吾輩は猫です。", "吾輩は犬です。") == [
        DiffChunk("equal", "吾輩は", "吾輩は"),
        DiffChunk("replace", "猫", "犬"),
        DiffChunk("equal", "です。", "です。"),
    ]


def test_render_html_escapes_text_and_renders_diff_chunks():
    html = render_html(
        [
            DiffChunk("equal", "", "<本文>"),
            DiffChunk("insert", "", "追記"),
            DiffChunk("replace", "旧文", "新版"),
            DiffChunk("delete", "削除", ""),
        ],
        "比較 <結果>",
    )

    assert "<本文>" not in html
    assert "&lt;本文&gt;" in html
    assert "<title>比較 &lt;結果&gt;</title>" in html
    assert '<span class="insert">追記</span>' in html
    assert 'data-old-text="旧文"' in html
    assert '<span class="delete">削除</span>' in html


def test_render_html_treats_brackets_as_plain_text():
    html = render_html(
        [DiffChunk("insert", "", "本文〔注釈〕")],
        "比較",
    )

    assert "本文〔注釈〕" in html
    assert "annotation" not in html


def test_render_html_supports_horizontal_layout():
    html = render_html(
        [DiffChunk("equal", "本文", "本文")],
        "比較",
        layout="horizontal",
    )

    assert "writing-mode: horizontal-tb" in html
    assert "max-width: 60em" in html
