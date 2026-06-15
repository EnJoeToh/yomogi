# かな変換・モーラ表示

読み候補の生成、人間による確認、モーラ表示の順で使用します。

## 1. 読み候補を作る

```console
yomogi kanaize novel.txt
```

`novel.kana.txt`を生成します。

- 漢字はひらがなの読みへ変換
- 元のひらがなは維持
- 元のカタカナは維持
- 数字、記号、改行は維持

読みは自動推定なので、生成後に人間が確認・修正してください。

## 2. モーラ表示を作る

```console
yomogi mora view novel.kana.txt
```

```text
novel.mora/
├── index.html
└── svg/
    ├── line-0001-mora.svg
    ├── line-0001-consonant.svg
    └── ...
```

一行につき次のSVGを生成します。

- モーラを表示するSVG
- 子音を表示するSVG

各セルは1モーラを表す正方形で、背景色は母音を示します。`index.html`上のボタンで表示を切り替えられます。

## VS Code Run on Save

[Run On Save](https://marketplace.visualstudio.com/items?itemName=emeraldwalk.RunOnSave)を使用する場合、ワークスペースの`.vscode/settings.json`へ追加します。

```json
{
  "emeraldwalk.runonsave": {
    "commands": [
      {
        "match": "\\.kana\\.txt$",
        "cmd": "yomogi mora view \"${file}\""
      }
    ]
  }
}
```

`.kana.txt`を保存するたびに、同じ場所の`.mora/`ディレクトリが更新されます。

## Live Server

[Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)で`novel.mora/index.html`を開くと、保存後の表示をブラウザで確認できます。

Run on SaveがSVGとHTMLを更新し、Live Serverがブラウザを再読み込みする構成です。
