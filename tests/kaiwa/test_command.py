from pathlib import Path

from yomogi.commands.kaiwa.command import default_output_path, main


def test_default_output_path_uses_kaiwa_markdown_suffix():
    assert default_output_path(Path("novel.txt")) == Path("novel.kaiwa.md")


def test_main_writes_markdown(tmp_path: Path):
    source = tmp_path / "novel.txt"
    source.write_text("前文。「台詞」後文。", encoding="utf-8")

    result = main([str(source)])

    output = tmp_path / "novel.kaiwa.md"
    assert result == 0
    assert "## 会話 1" in output.read_text(encoding="utf-8")
