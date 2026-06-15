import re
from collections.abc import Callable

from markupsafe import Markup

from yomogi.commands.scenario.models import (
    Conversation,
    DocumentTitle,
    Node,
    PartTitle,
    Scene,
    StageDirection,
    TextBlock,
)
from yomogi.commands.scenario.numbering import format_scene_number

Replacement = str | Callable[[re.Match[str]], str]

_STYLE_RULES: tuple[tuple[re.Pattern[str], Replacement], ...] = (
    (re.compile(r"〔\+\s*(.+?)〕"), r"<strong>\1</strong>"),
    (re.compile(r"〔-\s*(.+?)〕"), r"<del>\1</del>"),
    (re.compile(r"〔\*\s*(.+?)〕"), r'<span class="red">\1</span>'),
    (re.compile(r"〔#\s*(.+?)〕"), r'<span class="blue">\1</span>'),
    (re.compile(r"\[\+\s*(.+?)\]"), r"<strong>\1</strong>"),
    (re.compile(r"\[-\s*(.+?)\]"), r"<del>\1</del>"),
    (re.compile(r"\[\*\s*(.+?)\]"), r'<span class="red">\1</span>'),
    (re.compile(r"\[#\s*(.+?)\]"), r'<span class="blue">\1</span>'),
)
_LINK_PATTERN = re.compile(r"&gt;&gt;\s*(\d+(?:\.\d+)*)")


def render_inline(
    text: str,
    targets: dict[str, str] | None = None,
) -> Markup:
    escaped = str(Markup.escape(text))
    link_targets = targets or {}

    def replace_link(match: re.Match[str]) -> str:
        number = match.group(1)
        label, default_anchor = format_scene_number(number)
        anchor = link_targets.get(number, default_anchor)
        return (
            f'<a href="#{anchor}" class="scene-link">'
            f"&gt;&gt; {label}</a>"
        )

    rendered = _LINK_PATTERN.sub(replace_link, escaped)
    for pattern, replacement in _STYLE_RULES:
        rendered = pattern.sub(replacement, rendered)
    return Markup(rendered)


def apply_markup(nodes: list[Node], targets: dict[str, str]) -> None:
    for node in nodes:
        if isinstance(node, (DocumentTitle, PartTitle)):
            node.text = render_inline(str(node.text), targets)
            continue

        if not isinstance(node, Scene):
            continue

        node.text = render_inline(str(node.text), targets)
        for block in node.blocks:
            if isinstance(block, Conversation):
                block.speaker = render_inline(str(block.speaker), targets)
                block.text = render_inline(str(block.text), targets)
            elif isinstance(block, (StageDirection, TextBlock)):
                block.text = render_inline(str(block.text), targets)
