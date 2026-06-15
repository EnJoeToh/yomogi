from yomogi.commands.kaiwa.extractor import ConversationBlock
from yomogi.commands.kaiwa.renderer import render_markdown


def test_render_markdown_uses_numbered_sections():
    markdown = render_markdown(
        [
            ConversationBlock(("前文。", "「台詞」", "後文。")),
            ConversationBlock(("別の前文。", "「別の台詞」")),
        ]
    )

    assert markdown.startswith("# 会話抽出\n")
    assert "## 会話 1\n\n- 前文。\n- 「台詞」\n- 後文。" in markdown
    assert "\n\n---\n\n## 会話 2" in markdown
