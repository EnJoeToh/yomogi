def kanaize(text: str) -> str:
    """Convert kanji and hiragana to hiragana while preserving katakana."""
    import pykakasi

    converter = pykakasi.kakasi()
    return "".join(
        _kanaize_line(line, converter)
        for line in text.splitlines(keepends=True)
    )


def _kanaize_line(line: str, converter: object) -> str:
    ending = ""
    for candidate in ("\r\n", "\n", "\r"):
        if line.endswith(candidate):
            line = line[: -len(candidate)]
            ending = candidate
            break

    converted = converter.convert(line)
    output = []
    for item in converted:
        original = item["orig"]
        hiragana = item.get("hira", "")
        katakana = item.get("kana", "")

        if original == katakana:
            output.append(original)
        elif hiragana:
            output.append(hiragana)
        else:
            output.append(original)
    return "".join(output) + ending
