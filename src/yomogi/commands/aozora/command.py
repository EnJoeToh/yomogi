import argparse
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError

from yomogi.commands.aozora.catalog import CatalogError, find_work
from yomogi.commands.aozora.fetcher import download, filename_for
from yomogi.commands.aozora.extractor import (
    AozoraTextError,
    cleaned_path_for,
    extract_clean_text,
    extract_original_text,
    original_path_for,
)


CATALOG_RELATIVE_PATH = Path(
    "data/aozora/list_person_all_extended_utf8.csv"
)
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]


def resolve_catalog(path: Path | None) -> Path:
    if path is not None:
        return path

    search_roots = [Path.cwd(), *Path.cwd().parents, REPOSITORY_ROOT]
    for root in search_roots:
        candidate = root / CATALOG_RELATIVE_PATH
        if candidate.is_file():
            return candidate
    return CATALOG_RELATIVE_PATH


def build_parser(prog: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="Download works from Aozora Bunko.",
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    fetch_parser = subparsers.add_parser(
        "fetch",
        help="download a text ZIP by work ID",
    )
    fetch_parser.add_argument("work_id", help="Aozora Bunko work ID")
    fetch_parser.add_argument(
        "--catalog",
        type=Path,
        help=f"Aozora catalog CSV (default: {CATALOG_RELATIVE_PATH})",
    )
    fetch_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output ZIP path (default: filename from catalog URL)",
    )

    extract_parser = subparsers.add_parser(
        "extract",
        help="remove Aozora notes and footer from an original text",
    )
    extract_parser.add_argument(
        "original_path",
        type=Path,
        help="UTF-8 .org.txt file created by fetch",
    )
    extract_parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="cleaned text path (default: remove .org from input name)",
    )
    return parser


def fetch(
    args: argparse.Namespace,
    parser: argparse.ArgumentParser,
) -> tuple[Path, Path]:
    catalog = resolve_catalog(args.catalog)
    if not catalog.is_file():
        parser.error(f"catalog file not found: {catalog}")

    try:
        work = find_work(catalog, args.work_id)
        zip_output = args.output or Path(filename_for(work))
        original_output = original_path_for(zip_output)
        download(work, zip_output)
        extract_original_text(zip_output, original_output)
        return zip_output, original_output
    except (CatalogError, ValueError) as exc:
        parser.error(str(exc))
    except (OSError, HTTPError, URLError) as exc:
        parser.error(f"failed to download ZIP: {exc}")


def extract(
    args: argparse.Namespace,
    parser: argparse.ArgumentParser,
) -> Path:
    if not args.original_path.is_file():
        parser.error(f"input text not found: {args.original_path}")

    output = args.output or cleaned_path_for(args.original_path)
    try:
        unsupported = extract_clean_text(args.original_path, output)
        for annotation in unsupported:
            print(
                f"warning: unsupported annotation: {annotation}",
                file=sys.stderr,
            )
        return output
    except (AozoraTextError, OSError) as exc:
        parser.error(str(exc))


def main(argv: list[str] | None = None, prog: str | None = None) -> int:
    parser = build_parser(prog)
    args = parser.parse_args(argv)
    if args.action == "fetch":
        outputs = fetch(args, parser)
    else:
        outputs = (extract(args, parser),)

    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
