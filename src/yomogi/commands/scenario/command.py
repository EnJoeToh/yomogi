import argparse
import sys
from pathlib import Path

from jinja2 import TemplateNotFound

from yomogi.commands.scenario.markup import apply_markup
from yomogi.commands.scenario.numbering import (
    link_targets,
    prepare_numbering,
)
from yomogi.commands.scenario.docx_renderer import render_docx
from yomogi.commands.scenario.parser import parse_text
from yomogi.commands.scenario.renderer import DEFAULT_TEMPLATE, render_html


def decide_output_path(
    scenario_path: Path,
    output: Path | None,
    output_format: str = "html",
) -> Path:
    return output or scenario_path.with_suffix(f".{output_format}")


def build_parser(prog: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="シナリオtxtをHTMLまたはDOCXに整形します。",
    )
    parser.add_argument("scenario", type=Path, help="入力するシナリオtxt")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="出力パス",
    )
    parser.add_argument(
        "-t",
        "--template",
        default=DEFAULT_TEMPLATE,
        help=f"Jinja2テンプレート名 (default: {DEFAULT_TEMPLATE})",
    )
    parser.add_argument(
        "--format",
        choices=("html", "docx"),
        default="html",
        help="出力形式 (default: html)",
    )
    return parser


def main(argv: list[str] | None = None, prog: str | None = None) -> int:
    parser = build_parser(prog)
    args = parser.parse_args(argv)

    if not args.scenario.is_file():
        parser.error(f"input file not found: {args.scenario}")

    try:
        source_text = args.scenario.read_text(encoding="utf-8")
    except OSError as exc:
        parser.error(f"failed to read input: {exc}")

    nodes = parse_text(source_text)
    warnings = prepare_numbering(nodes, source_text)
    apply_markup(nodes, link_targets(nodes))

    output = decide_output_path(args.scenario, args.output, args.format)
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        if args.format == "docx":
            document = render_docx(nodes)
            document.save(output)
        else:
            html = render_html(
                nodes,
                page_title=output.stem,
                template_name=args.template,
            )
            output.write_text(html, encoding="utf-8")
    except TemplateNotFound:
        parser.error(f"template not found: {args.template}")
    except OSError as exc:
        parser.error(f"failed to write output: {exc}")

    for warning in warnings:
        print(f"warning: {warning.message}", file=sys.stderr)
    if args.format == "docx":
        print(f"→ {output} を生成しました（format: docx）")
    else:
        print(f"→ {output} を生成しました（template: {args.template}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
