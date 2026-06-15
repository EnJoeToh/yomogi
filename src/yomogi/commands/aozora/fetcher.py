from pathlib import Path
from shutil import copyfileobj
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from yomogi.commands.aozora.catalog import Work


USER_AGENT = "yomogi/0.1 (+https://www.aozora.gr.jp/)"


def filename_for(work: Work) -> str:
    filename = Path(urlparse(work.text_url).path).name
    if not filename.lower().endswith(".zip"):
        raise ValueError(f"text file URL is not a ZIP file: {work.text_url}")
    return filename


def download(work: Work, output: Path) -> None:
    request = Request(work.text_url, headers={"User-Agent": USER_AGENT})
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f".{output.name}.part")

    try:
        with urlopen(request) as response, temporary.open("wb") as destination:
            copyfileobj(response, destination)
        temporary.replace(output)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
