from yomogi.commands.scenario.markup import apply_markup, render_inline
from yomogi.commands.scenario.models import Conversation, Scene


def test_render_inline_supports_all_styles():
    rendered = render_inline(
        "〔+ 太字〕〔- 削除〕〔* 赤字〕〔# 青字〕"
        "[+ 太字2][- 削除2][* 赤字2][# 青字2]"
    )

    assert "<strong>太字</strong>" in rendered
    assert "<del>削除</del>" in rendered
    assert '<span class="red">赤字</span>' in rendered
    assert '<span class="blue">青字</span>' in rendered
    assert "<strong>太字2</strong>" in rendered
    assert "<del>削除2</del>" in rendered


def test_render_inline_escapes_untrusted_html_and_resolves_links():
    rendered = render_inline("<script>x</script> >> 100", {"100": "scene-100"})

    assert "<script>" not in rendered
    assert "&lt;script&gt;x&lt;/script&gt;" in rendered
    assert 'href="#scene-100"' in rendered


def test_apply_markup_runs_after_structural_parsing():
    scene = Scene(
        text="〔+ 導入〕",
        no="100",
        line=1,
        blocks=[Conversation("太郎", "〔# 青字〕")],
    )

    apply_markup([scene], {"100": "scene-100"})

    assert str(scene.text) == "<strong>導入</strong>"
    assert str(scene.blocks[0].text) == '<span class="blue">青字</span>'
