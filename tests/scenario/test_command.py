from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

from yomogi.commands.scenario.command import decide_output_path, main

WORD_NAMESPACE = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
WORD_NS = WORD_NAMESPACE["w"]


def paragraph_runs(
    paragraph: ElementTree.Element,
) -> list[tuple[str, str | None, str | None, str | None]]:
    runs = []
    for run in paragraph.findall("./w:r", WORD_NAMESPACE):
        text = "".join(
            node.text or ""
            for node in run.findall("./w:t", WORD_NAMESPACE)
        )
        color = run.find("./w:rPr/w:color", WORD_NAMESPACE)
        color_value = (
            color.attrib.get(f"{{{WORD_NS}}}val")
            if color is not None
            else None
        )
        fonts = run.find("./w:rPr/w:rFonts", WORD_NAMESPACE)
        font_value = (
            fonts.attrib.get(f"{{{WORD_NS}}}eastAsia")
            if fonts is not None
            else None
        )
        size = run.find("./w:rPr/w:sz", WORD_NAMESPACE)
        size_value = (
            size.attrib.get(f"{{{WORD_NS}}}val")
            if size is not None
            else None
        )
        runs.append((text, color_value, font_value, size_value))
    return runs


def test_default_output_path_uses_input_filename(tmp_path: Path):
    source = tmp_path / "scenario.txt"

    assert decide_output_path(source, None) == tmp_path / "scenario.html"


def test_docx_output_path_uses_input_filename(tmp_path: Path):
    source = tmp_path / "scenario.txt"

    assert decide_output_path(source, None, "docx") == tmp_path / "scenario.docx"


def test_main_renders_default_org_template(tmp_path: Path):
    source = tmp_path / "scenario.txt"
    source.write_text("☆ 題名\n\n■ 導入\n太郎「こんにちは」\n", encoding="utf-8")

    result = main([str(source)])

    assert result == 0
    html = source.with_suffix(".html").read_text(encoding="utf-8")
    assert "writing-mode: vertical-rl" in html
    assert "太郎" in html


def test_main_accepts_template_option(tmp_path: Path):
    source = tmp_path / "scenario.txt"
    output = tmp_path / "custom.html"
    source.write_text("■ 導入\n太郎「こんにちは」\n", encoding="utf-8")

    main(
        [
            str(source),
            "--template",
            "scenario_modern.html",
            "-o",
            str(output),
        ]
    )

    html = output.read_text(encoding="utf-8")
    assert 'class="page"' in html
    assert 'class="scene-no"' in html


def test_main_renders_docx(tmp_path: Path):
    source = tmp_path / "scenario.txt"
    source.write_text(
        "☆ 題名\n\n"
        "★ 第一部\n\n"
        "■ 〔* 導入〕\n"
        "＠ 〔# 部屋〕。\n"
        "太郎「こんにちは、〔* 赤〕と〔# 青〕」\n\n"
        "■ 次\n"
        "花子「はい」\n",
        encoding="utf-8",
    )

    result = main([str(source), "--format", "docx"])

    assert result == 0
    output = source.with_suffix(".docx")
    assert output.is_file()
    with ZipFile(output) as archive:
        document_xml = archive.read("word/document.xml").decode("utf-8")
        footer_xml = archive.read("word/footer1.xml").decode("utf-8")
    assert 'w:w="16838"' in document_xml
    assert 'w:h="11906"' in document_xml
    assert 'w:orient="landscape"' in document_xml
    assert 'w:top="3686"' in document_xml
    assert 'w:right="1985"' in document_xml
    assert 'w:bottom="3686"' in document_xml
    assert 'w:left="1701"' in document_xml
    assert 'w:val="tbRl"' in document_xml
    assert 'w:linePitch="328"' in document_xml
    assert 'w:charSpace="3420"' in document_xml
    assert 'w:type="snapToChars"' in document_xml
    assert "○" in document_xml
    assert "導入" in document_xml
    assert "太郎" in document_xml
    assert "こんにちは" in document_xml
    assert 'w:color w:val="FF0000"' in document_xml
    assert 'w:color w:val="0000FF"' in document_xml
    assert 'w:before="120"' not in document_xml
    assert 'w:before="240"' not in document_xml
    assert 'w:after="120"' not in document_xml
    assert 'w:after="160"' not in document_xml
    assert 'w:after="240"' not in document_xml
    assert "PAGE" in footer_xml

    root = ElementTree.fromstring(document_xml)
    paragraphs = root.findall(".//w:body/w:p", WORD_NAMESPACE)
    paragraph_texts = [
        "".join(
            text.text or ""
            for text in paragraph.findall(".//w:t", WORD_NAMESPACE)
        )
        for paragraph in paragraphs
    ]
    assert paragraph_texts == [
        "題名",
        "",
        "第一部",
        "",
        "○導入",
        "部屋。",
        "太郎「こんにちは、赤と青」",
        "",
        "○次",
        "花子「はい」",
    ]
    paragraph_indents = [
        paragraph.find("./w:pPr/w:ind", WORD_NAMESPACE)
        for paragraph in paragraphs
    ]
    assert paragraph_indents[0] is not None
    assert paragraph_indents[0].attrib[f"{{{WORD_NS}}}left"] == "210"
    assert paragraph_indents[2] is not None
    assert paragraph_indents[2].attrib[f"{{{WORD_NS}}}left"] == "210"
    assert paragraph_indents[5] is not None
    assert paragraph_indents[5].attrib[f"{{{WORD_NS}}}left"] == "420"
    assert paragraph_indents[6] is not None
    assert paragraph_indents[6].attrib[f"{{{WORD_NS}}}left"] == "210"
    assert paragraph_indents[6].attrib[f"{{{WORD_NS}}}hanging"] == "210"
    assert paragraph_indents[9] is not None
    assert paragraph_indents[9].attrib[f"{{{WORD_NS}}}left"] == "210"
    assert paragraph_indents[9].attrib[f"{{{WORD_NS}}}hanging"] == "210"

    assert paragraph_runs(paragraphs[4]) == [
        ("○", None, "游ゴシック", "22"),
        ("導入", "FF0000", "游ゴシック", "22"),
    ]
    assert paragraph_runs(paragraphs[5]) == [
        ("部屋", "0000FF", "游ゴシック", "21"),
        ("。", None, "游ゴシック", "21"),
    ]
    assert paragraph_runs(paragraphs[6]) == [
        ("太郎", None, "游ゴシック", "21"),
        ("「こんにちは、", None, "游明朝", "21"),
        ("赤", "FF0000", "游明朝", "21"),
        ("と", None, "游明朝", "21"),
        ("青", "0000FF", "游明朝", "21"),
        ("」", None, "游明朝", "21"),
    ]


def test_main_prints_duplicate_warnings_to_stderr(
    tmp_path: Path,
    capsys,
):
    source = tmp_path / "scenario.txt"
    source.write_text(
        "■ 100 最初\n本文\n\n■ 100 二番目\n>> 100\n",
        encoding="utf-8",
    )

    main([str(source)])

    captured = capsys.readouterr()
    assert "warning: duplicate scene number 100" in captured.err
    assert "warning: scene link 100 is ambiguous" in captured.err
