import argparse
from pathlib import Path

from yomogi.commands.kaiwa.extractor import extract_conversation_blocks
from yomogi.commands.kaiwa.renderer import render_markdown


def default_output_path(input_path: Path) -> Path:
    return input_path.with_suffix(".kaiwa.md")


def build_parser(prog: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Extract sentences around Japanese dialogue as Markdown.",
    )
    parser.add_argument("input", type=Path, help="input UTF-8 text file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output Markdown path (default: INPUT.kaiwa.md)",
    )
    return parser


def main(argv: list[str] | None = None, prog: str | None = None) -> int:
    parser = build_parser(prog)
    args = parser.parse_args(argv)

    if not args.input.is_file():
        parser.error(f"input file not found: {args.input}")

    try:
        text = args.input.read_text(encoding="utf-8")
        output = args.output or default_output_path(args.input)
        markdown = render_markdown(extract_conversation_blocks(text))
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(markdown, encoding="utf-8", newline="\n")
    except OSError as exc:
        parser.error(f"failed to process input: {exc}")

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
