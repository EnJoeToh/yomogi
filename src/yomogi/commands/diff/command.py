import argparse
from pathlib import Path

from yomogi.commands.diff.differ import compare
from yomogi.commands.diff.renderer import render_html


def build_parser(prog: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Render a word-level diff between two Japanese text files.",
    )
    parser.add_argument("old", type=Path, help="original text file")
    parser.add_argument("new", type=Path, help="revised text file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output HTML file (default: NEW.diff.html)",
    )
    parser.add_argument(
        "--layout",
        choices=("vertical", "horizontal"),
        default="vertical",
        help="writing direction (default: vertical)",
    )
    return parser


def main(argv: list[str] | None = None, prog: str | None = None) -> int:
    parser = build_parser(prog)
    args = parser.parse_args(argv)

    for path in (args.old, args.new):
        if not path.is_file():
            parser.error(f"input file not found: {path}")

    try:
        old_text = args.old.read_text(encoding="utf-8")
        new_text = args.new.read_text(encoding="utf-8")
    except OSError as exc:
        parser.error(f"failed to read input: {exc}")

    output = args.output or args.new.with_suffix(".diff.html")
    html = render_html(
        compare(old_text, new_text),
        title=f"{args.old.name} -> {args.new.name}",
        layout=args.layout,
    )

    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(html, encoding="utf-8")
    except OSError as exc:
        parser.error(f"failed to write output: {exc}")

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
