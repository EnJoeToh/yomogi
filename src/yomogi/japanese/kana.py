HIRAGANA = frozenset(
    "あいうえお"
    "かきくけこ"
    "さしすせそ"
    "たちつてと"
    "なにぬねの"
    "はひふへほ"
    "まみむめも"
    "やゆよ"
    "らりるれろ"
    "わゐゑを"
    "っゔん"
    "がぎぐげご"
    "ざじずぜぞ"
    "だぢづでど"
    "ばびぶべぼ"
    "ぱぴぷぺぽ"
    "ぁぃぅぇぉ"
    "ゃゅょ"
    "ゎゕゖ"
)
SMALL_KANA = frozenset("ぁぃぅぇぉゃゅょ")
SOKUON = "っ"
CHOON = "ー"
HATSUON = "ん"


def hiragana_to_katakana(text: str) -> str:
    return "".join(
        chr(ord(character) + 0x60)
        if "\u3041" <= character <= "\u3096"
        else character
        for character in text
    )


def katakana_to_hiragana(text: str) -> str:
    return "".join(
        chr(ord(character) - 0x60)
        if "\u30a1" <= character <= "\u30f6"
        else character
        for character in text
    )


KATAKANA = frozenset(hiragana_to_katakana(character) for character in HIRAGANA)
KANA = HIRAGANA | KATAKANA | {CHOON}
