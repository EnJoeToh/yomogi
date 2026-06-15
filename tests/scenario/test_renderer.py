from markupsafe import Markup

from yomogi.commands.scenario.models import (
    Conversation,
    Scene,
    StageDirection,
    TextBlock,
)
from yomogi.commands.scenario.renderer import render_html


def test_renderer_autoescapes_plain_text():
    scene = Scene(
        text="<script>",
        no="100",
        line=1,
        blocks=[TextBlock("<b>本文</b>")],
        no_str="100",
        id="scene-100",
    )

    html = render_html([scene], template_name="scenario_modern.html")

    assert "<script>" not in html
    assert "&lt;script&gt;" in html
    assert "&lt;b&gt;本文&lt;/b&gt;" in html


def test_renderer_allows_prepared_markup_only():
    scene = Scene(
        text=Markup("<strong>導入</strong>"),
        no="100",
        line=1,
        no_str="100",
        id="scene-100",
    )

    html = render_html([scene], template_name="scenario_classic.html")

    assert "<strong>導入</strong>" in html
    assert html.count("<article>") == 1
    assert html.count("</article>") == 1


def test_standard_template_pads_colored_markup():
    scene = Scene(
        text=Markup(
            '<span class="red">赤字</span>'
            '<span class="blue">青字</span>'
        ),
        no="100",
        line=1,
        no_str="100",
        id="scene-100",
    )

    html = render_html([scene], template_name="scenario_modern.html")

    assert html.count("padding-inline: 3em") == 2
    assert ".red {\n      display: inline-block;" in html
    assert ".blue {\n      display: inline-block;" in html


def test_renderer_uses_conversation_enclosure():
    scene = Scene(
        text="導入",
        no="100",
        line=1,
        no_str="100",
        id="scene-100",
        blocks=[
            Conversation("太郎（電話）", "聞こえる？", enclosure="quote"),
            Conversation("花子（小声）", "聞こえるよ", enclosure="parenthesis"),
        ],
    )

    html = render_html([scene], template_name="scenario_modern.html")

    assert "「聞こえる？」" in html
    assert "（聞こえるよ）" in html


def test_modern_template_adds_space_after_stage_direction_group():
    scene = Scene(
        text="導入",
        no="100",
        line=1,
        no_str="100",
        id="scene-100",
        blocks=[
            StageDirection("一つ目"),
            StageDirection("二つ目"),
            Conversation("太郎", "台詞"),
        ],
    )

    html = render_html([scene], template_name="scenario_modern.html")

    assert ".togaki {\n      margin: 0;" in html
    assert ".togaki-end {\n      margin-bottom: 1.5em;" in html
    assert "padding-left: 2em;" in html
    assert "box-sizing: border-box;" in html
    assert '<div class="togaki">一つ目</div>' in html
    assert '<div class="togaki togaki-end">二つ目</div>' in html
