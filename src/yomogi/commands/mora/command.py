import argparse
from pathlib import Path

from yomogi.commands.mora.html_renderer import render_html
from yomogi.commands.mora.svg_renderer import render_line_svg
from yomogi.japanese.mora import MoraAnalyzer


def viewer_output_path(input_path: Path) -> Path:
    name = input_path.name
    if name.endswith(".kana.txt"):
        name = name.removesuffix(".kana.txt")
    else:
        name = input_path.stem
    return input_path.with_name(f"{name}.mora")


def build_parser(prog: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Visualize mora structure as per-line SVG files.",
    )
    subparsers = parser.add_subparsers(dest="action", required=True)
    view_parser = subparsers.add_parser(
        "view",
        help="generate per-line SVG files and an HTML viewer",
    )
    view_parser.add_argument(
        "input",
        type=Path,
        help="reviewed hiragana/katakana UTF-8 text",
    )
    view_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: INPUT.mora)",
    )
    return parser


def render_view(args: argparse.Namespace) -> Path:
    output = args.output or viewer_output_path(args.input)
    svg_directory = output / "svg"
    svg_directory.mkdir(parents=True, exist_ok=True)

    analyzer = MoraAnalyzer()
    lines = [
        analyzer.analyze(line)
        for line in args.input.read_text(encoding="utf-8").splitlines()
    ]
    for line_number, line in enumerate(lines, 1):
        if not line.source:
            continue
        stem = f"line-{line_number:04d}"
        for mode in ("mora", "consonant"):
            svg = render_line_svg(line, mode, line_number)
            (svg_directory / f"{stem}-{mode}.svg").write_text(
                svg,
                encoding="utf-8",
                newline="\n",
            )

    index = output / "index.html"
    index.write_text(
        render_html(args.input, lines),
        encoding="utf-8",
        newline="\n",
    )
    return index


def main(argv: list[str] | None = None, prog: str | None = None) -> int:
    parser = build_parser(prog)
    args = parser.parse_args(argv)

    if not args.input.is_file():
        parser.error(f"input file not found: {args.input}")

    try:
        output = render_view(args)
    except (OSError, ValueError) as exc:
        parser.error(f"failed to process input: {exc}")

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
