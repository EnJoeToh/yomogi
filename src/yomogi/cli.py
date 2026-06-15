import argparse
import sys
from collections.abc import Callable, Sequence

from yomogi.commands.aozora import command as aozora_command
from yomogi.commands.diff import command as diff_command
from yomogi.commands.docx2txt import command as docx2txt_command
from yomogi.commands.kanaize import command as kanaize_command
from yomogi.commands.kaiwa import command as kaiwa_command
from yomogi.commands.mora import command as mora_command
from yomogi.commands.scenario import command as scenario_command

Command = Callable[[list[str] | None, str | None], int]

COMMANDS: dict[str, Command] = {
    "aozora": aozora_command.main,
    "diff": diff_command.main,
    "docx2txt": docx2txt_command.main,
    "kanaize": kanaize_command.main,
    "kaiwa": kaiwa_command.main,
    "mora": mora_command.main,
    "scenario": scenario_command.main,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="yomogi",
        description="Command-line tools for working with text.",
    )
    parser.add_argument("command", nargs="?", choices=COMMANDS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    parser = build_parser()

    if not args:
        parser.print_help()
        return 0

    if args[0] in {"-h", "--help"}:
        parser.print_help()
        return 0

    command = args.pop(0)
    if command not in COMMANDS:
        parser.error(f"unknown command: {command}")

    return COMMANDS[command](args, f"yomogi {command}")


if __name__ == "__main__":
    raise SystemExit(main())
