import pytest

from yomogi.japanese.reading import kanaize


@pytest.mark.parametrize(
    "source, expected",
    [
        ("「日本語」", "「にほんご」"),
        ("　ぜんかく はんかく", "　ぜんかく はんかく"),
        ("2025", "2025"),
        ("２０２５", "２０２５"),
        ("二千二十五", "にせんにじゅうご"),
        ("コンピューターだよ", "コンピューターだよ"),
        ("こんぴゅーたーだよ", "こんぴゅーたーだよ"),
        ("ーの", "ーの"),
        ("んー", "んー"),
        ("っー", "っー"),
    ],
)
def test_kanaize_preserves_katakana_and_symbols(source, expected):
    assert kanaize(source) == expected


def test_kanaize_processes_each_line_independently():
    assert kanaize("猫\n犬\n") == "ねこ\nいぬ\n"
    assert kanaize("一行目\n二行目\n三行目") == (
        "いちぎょうめ\nにぎょうめ\nさんぎょうめ"
    )
