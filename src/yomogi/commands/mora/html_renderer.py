from html import escape
from pathlib import Path

from yomogi.commands.mora.svg_renderer import VOWEL_COLORS
from yomogi.japanese.mora import MoraLine


def render_html(
    source_path: Path,
    lines: list[MoraLine],
) -> str:
    rows = []
    for line_number, line in enumerate(lines, 1):
        if not line.source:
            rows.append('<div class="blank-line"></div>')
            continue

        stem = f"line-{line_number:04d}"
        rows.append(
            '<section class="line">'
            f'<div class="line-label">{line_number:04d}</div>'
            '<div class="svg-scroll">'
            f'<img class="mora-view" src="svg/{stem}-mora.svg" '
            f'alt="line {line_number} mora">'
            f'<img class="consonant-view" src="svg/{stem}-consonant.svg" '
            f'alt="line {line_number} consonants" hidden>'
            "</div>"
            "</section>"
        )

    legend = "".join(
        '<span class="legend-item">'
        f'<i style="background:{color}"></i>{vowel.upper()}'
        "</span>"
        for vowel, color in VOWEL_COLORS.items()
    )
    body = "".join(rows) or "<p>表示する行がありません。</p>"
    title = f"Mora Viewer: {source_path.name}"

    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<style>
:root {{
  font-family: "Hiragino Sans", "Yu Gothic", "Noto Sans JP",
    system-ui, sans-serif;
  color: #111;
}}
* {{ box-sizing: border-box; }}
body {{ margin: 24px; }}
h1 {{ font-size: 1.2rem; }}
.toolbar, .legend {{ display: flex; gap: 8px; flex-wrap: wrap; }}
.toolbar {{ margin: 16px 0; }}
button {{
  border: 1px solid #aaa;
  border-radius: 4px;
  background: #fff;
  padding: 6px 12px;
  font: inherit;
  cursor: pointer;
}}
button[aria-pressed="true"] {{ background: #222; color: #fff; }}
.legend-item {{ display: inline-flex; gap: 4px; align-items: center; }}
.legend-item i {{
  width: 14px;
  height: 14px;
  border: 1px solid #aaa;
  border-radius: 3px;
}}
.line {{
  display: grid;
  grid-template-columns: 36px minmax(0, 1fr);
  gap: 4px;
  align-items: center;
  margin: 16px 0;
}}
.line-label {{ color: #666; font-family: monospace; font-size: 0.85rem; }}
.svg-scroll {{ overflow-x: auto; }}
.svg-scroll img {{ display: block; max-width: none; }}
.svg-scroll img[hidden] {{ display: none; }}
.blank-line {{ height: 24px; }}
</style>
</head>
<body>
<h1>{escape(title)}</h1>
<div class="toolbar" aria-label="表示切替">
  <button type="button" data-mode="mora" aria-pressed="true">Mora</button>
  <button type="button" data-mode="consonant" aria-pressed="false">Consonant</button>
</div>
<div class="legend">{legend}</div>
<main>{body}</main>
<script>
const buttons = document.querySelectorAll("[data-mode]");
const moraViews = document.querySelectorAll(".mora-view");
const consonantViews = document.querySelectorAll(".consonant-view");

function setMode(mode) {{
  const consonant = mode === "consonant";
  moraViews.forEach((view) => {{ view.hidden = consonant; }});
  consonantViews.forEach((view) => {{ view.hidden = !consonant; }});
  buttons.forEach((button) => {{
    button.setAttribute(
      "aria-pressed",
      String(button.dataset.mode === mode),
    );
  }});
}}

buttons.forEach((button) => {{
  button.addEventListener("click", () => setMode(button.dataset.mode));
}});
</script>
</body>
</html>
"""
