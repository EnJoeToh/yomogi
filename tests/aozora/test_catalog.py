from pathlib import Path

import pytest

from yomogi.commands.aozora.catalog import (
    WorkNotFoundError,
    find_work,
    normalize_work_id,
)


def write_catalog(path: Path, rows: list[str]) -> None:
    path.write_text(
        "作品ID,作品名,テキストファイルURL\n" + "\n".join(rows) + "\n",
        encoding="utf-8-sig",
    )


def test_normalize_work_id_adds_leading_zeroes():
    assert normalize_work_id("4088") == "004088"


def test_find_work_deduplicates_people_rows(tmp_path: Path):
    catalog = tmp_path / "catalog.csv"
    url = "https://www.aozora.gr.jp/cards/000601/files/4088_ruby_5542.zip"
    write_catalog(
        catalog,
        [
            f'004088,青草,{url}',
            f'004088,青草,{url}',
        ],
    )

    work = find_work(catalog, "4088")

    assert work.id == "004088"
    assert work.title == "青草"
    assert work.text_url == url


def test_find_work_reports_unknown_id(tmp_path: Path):
    catalog = tmp_path / "catalog.csv"
    write_catalog(catalog, [])

    with pytest.raises(WorkNotFoundError, match="9999"):
        find_work(catalog, "9999")
