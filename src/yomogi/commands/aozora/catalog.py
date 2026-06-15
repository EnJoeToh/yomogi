import csv
from dataclasses import dataclass
from pathlib import Path


class CatalogError(Exception):
    """Base error for Aozora catalog operations."""


class WorkNotFoundError(CatalogError):
    pass


class InvalidCatalogError(CatalogError):
    pass


@dataclass(frozen=True)
class Work:
    id: str
    title: str
    text_url: str


def normalize_work_id(value: str) -> str:
    if not value.isdigit():
        raise ValueError("work ID must contain only digits")
    return value.zfill(6)


def find_work(path: Path, work_id: str) -> Work:
    normalized_id = normalize_work_id(work_id)
    matches: dict[str, Work] = {}

    try:
        with path.open(encoding="utf-8-sig", newline="") as catalog:
            reader = csv.DictReader(catalog)
            required_columns = {"作品ID", "作品名", "テキストファイルURL"}
            if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
                raise InvalidCatalogError("catalog is missing required columns")

            for row in reader:
                if row["作品ID"] != normalized_id:
                    continue
                text_url = row["テキストファイルURL"].strip()
                if text_url:
                    matches[text_url] = Work(
                        id=normalized_id,
                        title=row["作品名"],
                        text_url=text_url,
                    )
    except (OSError, csv.Error) as exc:
        raise InvalidCatalogError(f"failed to read catalog: {exc}") from exc

    if not matches:
        raise WorkNotFoundError(f"work ID not found: {work_id}")
    if len(matches) > 1:
        raise InvalidCatalogError(
            f"work ID {work_id} has multiple text file URLs"
        )
    return next(iter(matches.values()))
