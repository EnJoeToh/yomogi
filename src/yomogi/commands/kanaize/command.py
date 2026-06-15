import argparse
from pathlib import Path

from yomogi.japanese.reading import kanaize


def output_path_for(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}.kana.txt")


def build_parser(prog: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Create a kana reading draft for manual review.",
    )
    parser.add_argument("input", type=Path, help="input UTF-8 text")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output text path (default: INPUT.kana.txt)",
    )
    return parser


def main(argv: list[str] | None = None, prog: str | None = None) -> int:
    parser = build_parser(prog)
    args = parser.parse_args(argv)

    if not args.input.is_file():
        parser.error(f"input file not found: {args.input}")

    output = args.output or output_path_for(args.input)
    try:
        text = args.input.read_text(encoding="utf-8")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(kanaize(text), encoding="utf-8", newline="\n")
    except OSError as exc:
        parser.error(f"failed to process input: {exc}")

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
