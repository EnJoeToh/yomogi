from yomogi.cli import build_parser


def test_cli_uses_yomogi_command_name():
    assert build_parser().prog == "yomogi"
