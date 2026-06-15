from pathlib import Path

from yomogi.commands.aozora import command


def write_catalog(path: Path, url: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "作品ID,作品名,テキストファイルURL\n"
        f"004088,青草,{url}\n",
        encoding="utf-8-sig",
    )


def test_fetch_downloads_work_to_url_filename(
    tmp_path: Path,
    monkeypatch,
    capsys,
):
    catalog = tmp_path / "catalog.csv"
    url = "https://www.aozora.gr.jp/cards/000601/files/4088_ruby_5542.zip"
    write_catalog(catalog, url)
    monkeypatch.chdir(tmp_path)
    downloaded = {}

    def fake_download(work, output):
        downloaded["work"] = work
        downloaded["output"] = output
        output.write_bytes(b"zip")

    def fake_extract_original(zip_path, output):
        downloaded["original_zip"] = zip_path
        downloaded["original_output"] = output
        output.write_text("original", encoding="utf-8")

    monkeypatch.setattr(command, "download", fake_download)
    monkeypatch.setattr(
        command,
        "extract_original_text",
        fake_extract_original,
    )

    result = command.main(["fetch", "4088", "--catalog", str(catalog)])

    output = tmp_path / "4088_ruby_5542.zip"
    assert result == 0
    assert downloaded["work"].title == "青草"
    assert downloaded["output"] == Path("4088_ruby_5542.zip")
    assert output.read_bytes() == b"zip"
    assert downloaded["original_zip"] == Path("4088_ruby_5542.zip")
    assert downloaded["original_output"] == Path("4088_ruby_5542.org.txt")
    assert capsys.readouterr().out == (
        "4088_ruby_5542.zip\n4088_ruby_5542.org.txt\n"
    )


def test_fetch_finds_default_catalog_outside_repository(
    tmp_path: Path,
    monkeypatch,
):
    repository = tmp_path / "repository"
    working_directory = tmp_path / "elsewhere"
    working_directory.mkdir()
    catalog = repository / command.CATALOG_RELATIVE_PATH
    url = "https://www.aozora.gr.jp/cards/000601/files/4088_ruby_5542.zip"
    write_catalog(catalog, url)
    monkeypatch.setattr(command, "REPOSITORY_ROOT", repository)
    monkeypatch.chdir(working_directory)
    downloaded = {}

    def fake_download(work, output):
        downloaded["work"] = work
        downloaded["output"] = output

    def fake_extract_original(zip_path, output):
        downloaded["original_output"] = output

    monkeypatch.setattr(command, "download", fake_download)
    monkeypatch.setattr(
        command,
        "extract_original_text",
        fake_extract_original,
    )

    result = command.main(["fetch", "4088"])

    assert result == 0
    assert downloaded["work"].title == "青草"
    assert downloaded["output"] == Path("4088_ruby_5542.zip")
    assert downloaded["original_output"] == Path("4088_ruby_5542.org.txt")


def test_extract_removes_org_from_default_output_name(
    tmp_path: Path,
    monkeypatch,
    capsys,
):
    original = tmp_path / "4088_ruby_5542.org.txt"
    original.write_text("original", encoding="utf-8")
    extracted = {}

    def fake_extract(original_path, output):
        extracted["original_path"] = original_path
        extracted["output"] = output
        return ()

    monkeypatch.setattr(command, "extract_clean_text", fake_extract)

    result = command.main(["extract", str(original)])

    assert result == 0
    assert extracted["original_path"] == original
    assert extracted["output"] == tmp_path / "4088_ruby_5542.txt"
    assert capsys.readouterr().out == f"{tmp_path / '4088_ruby_5542.txt'}\n"


def test_extract_warns_about_unsupported_annotations(
    tmp_path: Path,
    monkeypatch,
    capsys,
):
    original = tmp_path / "work.org.txt"
    original.write_text("original", encoding="utf-8")

    monkeypatch.setattr(
        command,
        "extract_clean_text",
        lambda _original, _output: ("［＃未対応］",),
    )

    command.main(["extract", str(original)])

    assert (
        capsys.readouterr().err
        == "warning: unsupported annotation: ［＃未対応］\n"
    )
