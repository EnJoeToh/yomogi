from xml.etree.ElementTree import Element, SubElement, tostring

from yomogi.japanese.mora import MoraLine


CELL_SIZE = 40
CELL_GAP = 3
VOWEL_COLORS = {
    "a": "#f8b4b4",
    "i": "#c3dafe",
    "u": "#c6f6d5",
    "e": "#fef3c7",
    "o": "#ddd6fe",
}
NEUTRAL_COLOR = "#eeeeee"


def render_line_svg(
    line: MoraLine,
    mode: str,
    line_number: int,
) -> str:
    if mode not in {"mora", "consonant"}:
        raise ValueError(f"unknown SVG mode: {mode}")

    cell_count = max(1, len(line.moras))
    width = cell_count * CELL_SIZE + (cell_count - 1) * CELL_GAP
    root = Element(
        "svg",
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "width": str(width),
            "height": str(CELL_SIZE),
            "viewBox": f"0 0 {width} {CELL_SIZE}",
            "role": "img",
            "aria-label": f"line {line_number} {mode}",
        },
    )
    title = SubElement(root, "title")
    title.text = f"Line {line_number}: {mode}"

    for index, mora in enumerate(line.moras):
        x = index * (CELL_SIZE + CELL_GAP)
        SubElement(
            root,
            "rect",
            {
                "x": str(x),
                "y": "0",
                "width": str(CELL_SIZE),
                "height": str(CELL_SIZE),
                "fill": VOWEL_COLORS.get(mora.vowel, NEUTRAL_COLOR),
                "stroke": "#888888",
                "rx": "5",
                "ry": "5",
            },
        )
        label = mora.text if mode == "mora" else mora.consonant
        text = SubElement(
            root,
            "text",
            {
                "x": str(x + CELL_SIZE / 2),
                "y": str(CELL_SIZE / 2),
                "text-anchor": "middle",
                "dominant-baseline": "central",
                "font-family": (
                    "Hiragino Sans, Yu Gothic, Noto Sans JP, "
                    "system-ui, sans-serif"
                ),
                "font-size": "16",
                "fill": "#111111",
            },
        )
        text.text = label

    return tostring(root, encoding="unicode", xml_declaration=False) + "\n"
