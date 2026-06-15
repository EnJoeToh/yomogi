# シナリオ整形

UTF-8のシナリオテキストをHTMLへ変換します。

```console
yomogi scenario sample.scenario.txt
```

既定では`sample.scenario.html`を生成します。

## 入力記法

```text
☆ 作品タイトル
★ 第一部

■ 100 導入
＠ 部屋の中。
太郎「こんにちは」
花子（聞こえる？）
通常の本文
```

| 記法 | 意味 |
|---|---|
| `☆` | 文書タイトル |
| `★` | 部タイトル |
| `■ 100 見出し` | シーン番号と見出し |
| `■ 見出し` | 自動採番するシーン |
| `＠` | ト書き |
| `名前「台詞」` | 通常の会話 |
| `名前（台詞）` | 括弧付きの会話 |

シーン参照には`>> 100`を使用できます。

## テンプレート

```console
yomogi scenario sample.scenario.txt --template scenario_modern.html
```

利用できるテンプレート:

- `scenario_classic.html`
- `scenario_modern.html`

## VS Code Run on Save

[Run On Save](https://marketplace.visualstudio.com/items?itemName=emeraldwalk.RunOnSave)を使用する場合、ワークスペースの`.vscode/settings.json`へ追加します。

```json
{
  "emeraldwalk.runonsave": {
    "commands": [
      {
        "match": "\\.scenario\\.txt$",
        "cmd": "yomogi scenario \"${file}\""
      }
    ]
  }
}
```

モダンテンプレートを使用する場合:

```json
{
  "emeraldwalk.runonsave": {
    "commands": [
      {
        "match": "\\.scenario\\.txt$",
        "cmd": "yomogi scenario \"${file}\" --template scenario_modern.html"
      }
    ]
  }
}
```

## Live Server

[Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)で生成された`sample.scenario.html`を開くと、保存後の表示をブラウザで確認できます。
