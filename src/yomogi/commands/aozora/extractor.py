import re
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from yomogi.commands.aozora.notation import convert_notation


DELIMITER_PATTERN = re.compile(r"^\s*-{20,}\s*$")
FOOTER_START_PATTERN = re.compile(r"^底本(?:名)?[：:]")
AOZORA_FOOTER_MARKERS = (
    "青空文庫作成ファイル",
    "このファイルは、インターネットの図書館、青空文庫",
)


class AozoraTextError(Exception):
    """Raised when an Aozora text archive cannot be processed."""


def decode_text(data: bytes) -> str:
    for encoding in ("utf-8-sig", "cp932", "shift_jis"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise AozoraTextError("text encoding is not UTF-8 or Shift_JIS")


def strip_note_block(lines: list[str]) -> list[str]:
    opening = next(
        (
            index
            for index, line in enumerate(lines)
            if DELIMITER_PATTERN.fullmatch(line)
        ),
        None,
    )
    if opening is None:
        return lines

    closing = next(
        (
            index
            for index in range(opening + 1, len(lines))
            if DELIMITER_PATTERN.fullmatch(lines[index])
        ),
        None,
    )
    if closing is None:
        return lines

    end = closing + 1
    while end < len(lines) and not lines[end].strip():
        end += 1
    return lines[:opening] + lines[end:]


def strip_footer(lines: list[str]) -> list[str]:
    marker_index = next(
        (
            index
            for index in range(len(lines) - 1, -1, -1)
            if any(marker in lines[index] for marker in AOZORA_FOOTER_MARKERS)
        ),
        None,
    )
    if marker_index is None:
        return lines

    footer_start = next(
        (
            index
            for index in range(marker_index, -1, -1)
            if FOOTER_START_PATTERN.match(lines[index].strip())
        ),
        marker_index,
    )
    while footer_start > 0 and not lines[footer_start - 1].strip():
        footer_start -= 1
    return lines[:footer_start]


def clean_text(text: str) -> str:
    lines = normalize_text(text).splitlines()
    lines = strip_footer(strip_note_block(lines))

    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines) + ("\n" if lines else "")


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def read_text_from_zip(path: Path) -> str:
    try:
        with ZipFile(path) as archive:
            members = [
                member
                for member in archive.infolist()
                if not member.is_dir()
                and Path(member.filename).suffix.lower() == ".txt"
                and "__MACOSX" not in Path(member.filename).parts
            ]
            if not members:
                raise AozoraTextError("ZIP archive contains no text file")
            if len(members) > 1:
                names = ", ".join(member.filename for member in members)
                raise AozoraTextError(
                    f"ZIP archive contains multiple text files: {names}"
                )
            return decode_text(archive.read(members[0]))
    except (BadZipFile, OSError) as exc:
        raise AozoraTextError(f"failed to read ZIP archive: {exc}") from exc


def original_path_for(zip_path: Path) -> Path:
    return zip_path.with_suffix(".org.txt")


def extract_original_text(zip_path: Path, output: Path) -> None:
    original_text = normalize_text(read_text_from_zip(zip_path))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(original_text, encoding="utf-8", newline="\n")


def cleaned_path_for(original_path: Path) -> Path:
    if original_path.name.endswith(".org.txt"):
        return original_path.with_name(
            original_path.name.removesuffix(".org.txt") + ".txt"
        )
    return original_path.with_suffix(".txt")


def extract_clean_text(
    original_path: Path,
    output: Path,
) -> tuple[str, ...]:
    text = original_path.read_text(encoding="utf-8")
    result = convert_notation(clean_text(text))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(result.text, encoding="utf-8", newline="\n")
    return result.unsupported_annotations
