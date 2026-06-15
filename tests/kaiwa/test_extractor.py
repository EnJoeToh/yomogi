from yomogi.commands.kaiwa.extractor import (
    collect_sentences,
    dialogue_context_ranges,
    extract_conversation_blocks,
    split_line_into_sentences,
)


def test_split_line_does_not_split_inside_dialogue():
    assert split_line_into_sentences(
        "太郎は「本当か？　驚いた！」と言った。次の文。"
    ) == [
        "太郎は「本当か？　驚いた！」と言った。",
        "次の文。",
    ]


def test_collect_sentences_splits_each_line():
    assert collect_sentences("一文目。二文目。\n三文目。") == [
        "一文目。",
        "二文目。",
        "三文目。",
    ]


def test_overlapping_dialogue_context_ranges_are_merged():
    sentences = [
        "文1。",
        "「台詞A」",
        "文2。",
        "「台詞B」",
        "文3。",
    ]

    assert dialogue_context_ranges(sentences) == [(0, 4)]


def test_separate_dialogue_contexts_remain_separate():
    sentences = [
        "前文A。",
        "「台詞A」",
        "後文A。",
        "離れた文1。",
        "離れた文2。",
        "前文B。",
        "「台詞B」",
        "後文B。",
    ]

    assert dialogue_context_ranges(sentences) == [(0, 2), (5, 7)]


def test_extract_blocks_does_not_duplicate_shared_context():
    blocks = extract_conversation_blocks(
        "文1。「台詞A」文2。「台詞B」文3。"
    )

    assert len(blocks) == 1
    assert blocks[0].sentences == (
        "文1。",
        "「台詞A」文2。",
        "「台詞B」文3。",
    )
