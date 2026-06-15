import pytest

from yomogi.japanese.mora import MoraAnalyzer


@pytest.mark.parametrize(
    "text, expected_moras, expected_vowels",
    [
        ("かぉ", ["か", "ぉ"], ["a", "ぉ"]),
        ("かわ", ["か", "わ"], ["a", "a"]),
        ("ティー", ["てぃ", "い"], ["i", "i"]),
        ("そうかぁと", ["そ", "う", "か", "ぁ", "と"], ["o", "u", "a", "ぁ", "o"]),
        ("リィ", ["り", "ぃ"], ["i", "ぃ"]),
        ("だよ", ["だ", "よ"], ["a", "o"]),
        (
            "フィレオフィッシュ",
            ["ふぃ", "れ", "お", "ふぃ", "っ", "しゅ"],
            ["i", "e", "o", "i", "っ", "u"],
        ),
        ("ツァトゥグア", ["つぁ", "とぅ", "ぐ", "あ"], ["a", "u", "u", "a"]),
    ],
)
def test_analyze_moras(text, expected_moras, expected_vowels):
    line = MoraAnalyzer().analyze(text)

    assert [mora.text for mora in line.moras] == expected_moras
    assert [mora.vowel for mora in line.moras] == expected_vowels


def test_analyze_keeps_mora_cv_values_together():
    line = MoraAnalyzer().analyze("かな")

    assert [
        (mora.text, mora.consonant, mora.vowel)
        for mora in line.moras
    ] == [("か", "k", "a"), ("な", "n", "a")]
