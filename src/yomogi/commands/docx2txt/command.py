import argparse
import re
from pathlib import Path

import docx


def docx_to_text(path: Path) -> str:
    """Extract paragraphs from a DOCX file as newline-separated text."""
    document = docx.Document(path)
    paragraphs = [
        re.sub(r"^ ", "　", paragraph.text)
        for paragraph in document.paragraphs
    ]
    return "\n".join(paragraphs)


def build_parser(prog: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Extract paragraph text from a DOCX file."
    )
    parser.add_argument("input", type=Path, help="input DOCX file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output text file (default: standard output)",
    )
    return parser


def main(argv: list[str] | None = None, prog: str | None = None) -> int:
    parser = build_parser(prog)
    args = parser.parse_args(argv)

    if not args.input.is_file():
        parser.error(f"input file not found: {args.input}")

    try:
        text = docx_to_text(args.input)
    except (OSError, ValueError, KeyError) as exc:
        parser.error(f"failed to read DOCX: {exc}")

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
