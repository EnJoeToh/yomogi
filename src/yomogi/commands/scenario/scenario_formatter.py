"""Compatibility imports for the original scenario formatter module."""

from markupsafe import Markup

from yomogi.commands.scenario.command import (
    build_parser,
    decide_output_path,
    main,
)
from yomogi.commands.scenario.markup import render_inline
from yomogi.commands.scenario.numbering import (
    assign_dialogue_numbers,
    assign_scene_ids,
    assign_scene_numbers,
    collect_warnings,
    format_scene_number,
)
from yomogi.commands.scenario.parser import parse_lines, parse_text
from yomogi.commands.scenario.renderer import DEFAULT_TEMPLATE, render_html


def esc(text: str) -> str:
    return str(Markup.escape(text))


def apply_inline(text: str) -> str:
    return str(render_inline(text))


format_scene_numbers = assign_scene_ids
assign_global_serihu_numbers = assign_dialogue_numbers
collect_scene_warnings = collect_warnings


if __name__ == "__main__":
    raise SystemExit(main())
