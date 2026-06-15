from xml.etree.ElementTree import fromstring

from yomogi.commands.mora.svg_renderer import CELL_SIZE, render_line_svg
from yomogi.commands.mora.svg_renderer import CELL_GAP
from yomogi.japanese.mora import MoraAnalyzer


SVG_NAMESPACE = {"svg": "http://www.w3.org/2000/svg"}


def test_mora_svg_uses_one_square_per_mora():
    line = MoraAnalyzer().analyze("かな")
    root = fromstring(render_line_svg(line, "mora", 1))
    rectangles = root.findall("svg:rect", SVG_NAMESPACE)
    labels = root.findall("svg:text", SVG_NAMESPACE)

    assert root.attrib["width"] == str(2 * CELL_SIZE + CELL_GAP)
    assert root.attrib["height"] == str(CELL_SIZE)
    assert len(rectangles) == 2
    assert all(
        rectangle.attrib["width"] == rectangle.attrib["height"]
        for rectangle in rectangles
    )
    assert all(rectangle.attrib["rx"] == "5" for rectangle in rectangles)
    assert [rectangle.attrib["x"] for rectangle in rectangles] == [
        "0",
        str(CELL_SIZE + CELL_GAP),
    ]
    assert "Yu Gothic" in labels[0].attrib["font-family"]
    assert [label.text for label in labels] == ["か", "な"]
    assert [rectangle.attrib["fill"] for rectangle in rectangles] == [
        "#f8b4b4",
        "#f8b4b4",
    ]


def test_consonant_svg_uses_same_cells_with_consonant_labels():
    line = MoraAnalyzer().analyze("かな")
    root = fromstring(render_line_svg(line, "consonant", 1))
    labels = root.findall("svg:text", SVG_NAMESPACE)

    assert [label.text for label in labels] == ["k", "n"]
