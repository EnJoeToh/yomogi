from pathlib import Path

from yomogi.commands.mora.html_renderer import render_html
from yomogi.japanese.mora import MoraAnalyzer


def test_html_references_both_svg_modes():
    lines = [MoraAnalyzer().analyze("かな")]

    html = render_html(Path("sample.kana.txt"), lines)

    assert 'src="svg/line-0001-mora.svg"' in html
    assert 'src="svg/line-0001-consonant.svg"' in html
    assert 'data-mode="mora"' in html
    assert 'data-mode="consonant"' in html
    assert "overflow-x: auto" in html
    assert ".svg-scroll img[hidden] { display: none; }" in html
    assert '<div class="source">' not in html
    assert '<div class="line-label">0001</div>' in html
    assert '"Yu Gothic"' in html
