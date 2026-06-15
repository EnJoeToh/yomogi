from pathlib import Path

from yomogi.commands.scenario.command import decide_output_path, main


def test_default_output_path_uses_input_filename(tmp_path: Path):
    source = tmp_path / "scenario.txt"

    assert decide_output_path(source, None) == tmp_path / "scenario.html"


def test_main_renders_default_org_template(tmp_path: Path):
    source = tmp_path / "scenario.txt"
    source.write_text("☆ 題名\n\n■ 導入\n太郎「こんにちは」\n", encoding="utf-8")

    result = main([str(source)])

    assert result == 0
    html = source.with_suffix(".html").read_text(encoding="utf-8")
    assert "writing-mode: vertical-rl" in html
    assert "太郎" in html


def test_main_accepts_template_option(tmp_path: Path):
    source = tmp_path / "scenario.txt"
    output = tmp_path / "custom.html"
    source.write_text("■ 導入\n太郎「こんにちは」\n", encoding="utf-8")

    main(
        [
            str(source),
            "--template",
            "scenario_modern.html",
            "-o",
            str(output),
        ]
    )

    html = output.read_text(encoding="utf-8")
    assert 'class="page"' in html
    assert 'class="scene-no"' in html


def test_main_prints_duplicate_warnings_to_stderr(
    tmp_path: Path,
    capsys,
):
    source = tmp_path / "scenario.txt"
    source.write_text(
        "■ 100 最初\n本文\n\n■ 100 二番目\n>> 100\n",
        encoding="utf-8",
    )

    main([str(source)])

    captured = capsys.readouterr()
    assert "warning: duplicate scene number 100" in captured.err
    assert "warning: scene link 100 is ambiguous" in captured.err
