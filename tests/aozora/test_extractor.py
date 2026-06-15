from pathlib import Path
from zipfile import ZipFile

import pytest

from yomogi.commands.aozora.extractor import (
    AozoraTextError,
    clean_text,
    extract_clean_text,
    extract_original_text,
)


SOURCE = """作品名
著者名

-------------------------------------------------------
【テキスト中に現れる記号について】
《》：ルビ
-------------------------------------------------------

本文一行目。

本文二行目。

底本：「底本名」
出版社：出版社名
入力：入力者
校正：校正者
青空文庫作成ファイル：
このファイルは、インターネットの図書館、青空文庫で作られました。
"""


def test_clean_text_removes_header_notes_and_footer():
    assert clean_text(SOURCE) == (
        "作品名\n著者名\n\n本文一行目。\n\n本文二行目。\n"
    )


def test_extract_original_text_converts_shift_jis_zip_to_utf8(tmp_path: Path):
    archive = tmp_path / "4088.zip"
    original = tmp_path / "4088.org.txt"
    with ZipFile(archive, "w") as zip_file:
        zip_file.writestr("4088_ruby.txt", SOURCE.encode("cp932"))

    extract_original_text(archive, original)

    assert original.read_bytes() == SOURCE.encode("utf-8")


def test_extract_clean_text_uses_original_file(tmp_path: Path):
    original = tmp_path / "4088.org.txt"
    cleaned = tmp_path / "4088.txt"
    original.write_text(
        SOURCE.replace("本文一行目。", "｜本文《ほんぶん》［＃２字下げ］一行目。"),
        encoding="utf-8",
    )

    unsupported = extract_clean_text(original, cleaned)

    assert cleaned.read_text(encoding="utf-8") == (
        "作品名\n著者名\n\n本文　　一行目。\n\n本文二行目。\n"
    )
    assert unsupported == ()


def test_extract_rejects_zip_with_multiple_text_files(tmp_path: Path):
    archive = tmp_path / "multiple.zip"
    with ZipFile(archive, "w") as zip_file:
        zip_file.writestr("one.txt", b"one")
        zip_file.writestr("two.txt", b"two")

    with pytest.raises(AozoraTextError, match="multiple text files"):
        extract_original_text(archive, tmp_path / "output.org.txt")
