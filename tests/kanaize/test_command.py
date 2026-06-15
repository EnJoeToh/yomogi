from pathlib import Path

from yomogi.commands.kanaize.command import main, output_path_for


def test_default_output_path():
    assert output_path_for(Path("novel.txt")) == Path("novel.kana.txt")


def test_main_writes_reviewable_text(tmp_path: Path):
    source = tmp_path / "novel.txt"
    source.write_text("日本語とカタカナ", encoding="utf-8")

    result = main([str(source)])

    assert result == 0
    assert (tmp_path / "novel.kana.txt").read_text(
        encoding="utf-8"
    ) == "にほんごとカタカナ"
