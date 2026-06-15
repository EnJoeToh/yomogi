from io import BytesIO
from pathlib import Path

import pytest

from yomogi.commands.aozora import fetcher
from yomogi.commands.aozora.catalog import Work


@pytest.fixture
def work():
    return Work(
        id="004088",
        title="青草",
        text_url=(
            "https://www.aozora.gr.jp/cards/000601/"
            "files/4088_ruby_5542.zip"
        ),
    )


def test_download_saves_response_body(tmp_path: Path, monkeypatch, work):
    output = tmp_path / "downloads" / "work.zip"
    requested = {}

    def fake_urlopen(request):
        requested["url"] = request.full_url
        requested["user_agent"] = request.get_header("User-agent")
        return BytesIO(b"zip data")

    monkeypatch.setattr(fetcher, "urlopen", fake_urlopen)

    fetcher.download(work, output)

    assert output.read_bytes() == b"zip data"
    assert requested["url"] == work.text_url
    assert requested["user_agent"] == fetcher.USER_AGENT


def test_download_preserves_existing_file_on_failure(
    tmp_path: Path,
    monkeypatch,
    work,
):
    output = tmp_path / "work.zip"
    output.write_bytes(b"existing")

    def fail(_request):
        raise OSError("network failed")

    monkeypatch.setattr(fetcher, "urlopen", fail)

    with pytest.raises(OSError, match="network failed"):
        fetcher.download(work, output)

    assert output.read_bytes() == b"existing"
    assert not (tmp_path / ".work.zip.part").exists()
