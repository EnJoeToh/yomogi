from dataclasses import dataclass


SENTENCE_ENDINGS = "。？！"


@dataclass(frozen=True)
class ConversationBlock:
    sentences: tuple[str, ...]


def split_line_into_sentences(line: str) -> list[str]:
    sentences: list[str] = []
    buffer: list[str] = []
    in_dialogue = False

    for character in line:
        buffer.append(character)
        if character == "「":
            in_dialogue = True
        elif character == "」":
            in_dialogue = False

        if not in_dialogue and character in SENTENCE_ENDINGS:
            sentences.append("".join(buffer))
            buffer.clear()

    if buffer:
        sentences.append("".join(buffer))
    return sentences


def collect_sentences(text: str) -> list[str]:
    sentences: list[str] = []
    for line in text.splitlines():
        sentences.extend(
            sentence
            for sentence in split_line_into_sentences(line)
            if sentence
        )
    return sentences


def contains_dialogue(sentence: str) -> bool:
    return "「" in sentence and "」" in sentence


def dialogue_context_ranges(
    sentences: list[str],
) -> list[tuple[int, int]]:
    ranges = [
        (
            max(0, index - 1),
            min(len(sentences) - 1, index + 1),
        )
        for index, sentence in enumerate(sentences)
        if contains_dialogue(sentence)
    ]
    if not ranges:
        return []

    merged = [ranges[0]]
    for start, end in ranges[1:]:
        previous_start, previous_end = merged[-1]
        if start <= previous_end + 1:
            merged[-1] = (previous_start, max(previous_end, end))
        else:
            merged.append((start, end))
    return merged


def extract_conversation_blocks(text: str) -> list[ConversationBlock]:
    sentences = collect_sentences(text)
    return [
        ConversationBlock(tuple(sentences[start : end + 1]))
        for start, end in dialogue_context_ranges(sentences)
    ]
