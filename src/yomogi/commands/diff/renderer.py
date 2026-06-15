from dataclasses import dataclass
from typing import Literal

from jinja2 import Environment, PackageLoader, select_autoescape

from yomogi.commands.diff.differ import DiffChunk, DiffTag

Layout = Literal["vertical", "horizontal"]

_ENVIRONMENT = Environment(
    loader=PackageLoader("yomogi.commands.diff", "templates"),
    autoescape=select_autoescape(("html", "xml")),
    keep_trailing_newline=True,
)


@dataclass(frozen=True)
class RenderChunk:
    tag: DiffTag
    old_text: str
    new_text: str


def render_html(
    chunks: list[DiffChunk],
    title: str,
    layout: Layout = "vertical",
) -> str:
    render_chunks = [
        RenderChunk(
            tag=chunk.tag,
            old_text=chunk.old_text,
            new_text=chunk.new_text,
        )
        for chunk in chunks
    ]
    template = _ENVIRONMENT.get_template(f"diff_{layout}.html")
    return template.render(title=title, chunks=render_chunks)
