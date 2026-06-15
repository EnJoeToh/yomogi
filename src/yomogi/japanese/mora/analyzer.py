from yomogi.japanese.kana import CHOON, HIRAGANA, SMALL_KANA, SOKUON
from yomogi.japanese.kana import katakana_to_hiragana
from yomogi.japanese.mora.mapping import MoraMap, load_mora_map
from yomogi.japanese.mora.models import Mora, MoraLine


class MoraAnalyzer:
    def __init__(self, mora_map: MoraMap | None = None):
        self._mora_map = mora_map or load_mora_map()
        self._vowel_kana = {
            entry["V"]: kana
            for kana, entry in self._mora_map.items()
            if entry.get("is_vowel") is True
            and isinstance(entry.get("V"), str)
        }

    def split_moras(self, text: str) -> list[str]:
        hiragana = katakana_to_hiragana(text)
        moras: list[str] = []

        for character in hiragana:
            if character not in HIRAGANA and character != CHOON:
                moras.append(character)
                continue

            if character == SOKUON:
                moras.append(character)
                continue

            if character == CHOON:
                if moras:
                    previous = self._mora_map.get(moras[-1])
                    vowel = previous.get("V") if previous else None
                    vowel_kana = self._vowel_kana.get(vowel)
                    if vowel_kana:
                        moras.append(vowel_kana)
                        continue
                moras.append(character)
                continue

            if character in SMALL_KANA:
                combined = moras[-1] + character if moras else character
                if moras and combined in self._mora_map:
                    moras[-1] = combined
                else:
                    moras.append(character)
                continue

            moras.append(character)

        return moras

    def analyze(self, text: str) -> MoraLine:
        moras = []
        for text_mora in self.split_moras(text):
            entry = self._mora_map.get(text_mora)
            moras.append(
                Mora(
                    text=text_mora,
                    consonant=entry["C"] if entry else text_mora,
                    vowel=entry["V"] if entry else text_mora,
                )
            )
        return MoraLine(source=text, moras=tuple(moras))
