from yomogi.commands.kaiwa.extractor import ConversationBlock


def render_markdown(blocks: list[ConversationBlock]) -> str:
    sections = []
    for index, block in enumerate(blocks, 1):
        body = "\n".join(f"- {sentence}" for sentence in block.sentences)
        sections.append(f"## 会話 {index}\n\n{body}")

    if not sections:
        return "# 会話抽出\n\n会話を含む文は見つかりませんでした。\n"
    return "# 会話抽出\n\n" + "\n\n---\n\n".join(sections) + "\n"
