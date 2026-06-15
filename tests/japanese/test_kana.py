from yomogi.japanese.kana import (
    hiragana_to_katakana,
    katakana_to_hiragana,
)


def test_hiragana_and_katakana_conversion():
    assert hiragana_to_katakana("かなABC") == "カナABC"
    assert katakana_to_hiragana("カナABC") == "かなABC"
