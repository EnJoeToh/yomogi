from pathlib import Path

from yomogi.commands.mora.command import (
    main,
    viewer_output_path,
)


def test_default_output_path():
    assert viewer_output_path(Path("novel.kana.txt")) == Path("novel.mora")


def test_view_writes_two_svgs_per_nonblank_line_and_html(tmp_path: Path):
    source = tmp_path / "novel.kana.txt"
    source.write_text("かな\n\nモーラ\n", encoding="utf-8")

    result = main(["view", str(source)])

    output = tmp_path / "novel.mora"
    assert result == 0
    assert (output / "index.html").is_file()
    assert (output / "svg/line-0001-mora.svg").is_file()
    assert (output / "svg/line-0001-consonant.svg").is_file()
    assert not (output / "svg/line-0002-mora.svg").exists()
    assert (output / "svg/line-0003-mora.svg").is_file()
