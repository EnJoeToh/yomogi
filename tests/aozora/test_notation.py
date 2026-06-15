from yomogi.commands.aozora.notation import convert_notation


def test_convert_notation_removes_ruby_and_applies_annotations():
    result = convert_notation(
        "｜青空《あおぞら》"
        "［＃２字下げ］本文"
        "［＃「章」は中見出し］"
        "［＃「目＋爭」、第3水準1-88-85］"
    )

    assert result.text == "青空　　本文睜"
    assert result.unsupported_annotations == ()


def test_convert_notation_preserves_and_reports_unknown_annotations():
    result = convert_notation("本文［＃未対応の注記］")

    assert result.text == "本文［＃未対応の注記］"
    assert result.unsupported_annotations == ("［＃未対応の注記］",)
