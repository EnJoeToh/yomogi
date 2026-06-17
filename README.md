# Yomogi

日本語テキストを扱うためのコマンドラインツール集です。

## 必要環境

- Python 3.10以上
- [pipx](https://pipx.pypa.io/)

## インストール

GitHubからインストールする場合:

```console
pipx install git+https://github.com/EnJoeToh/yomogi.git
```

ローカルで開発する場合:

```console
git clone https://github.com/EnJoeToh/yomogi.git
cd yomogi
pipx install --editable .
```

## コマンド

| コマンド | 用途 |
|---|---|
| `yomogi aozora` | 青空文庫の作品取得とテキスト整形 |
| `yomogi diff` | 日本語テキストの語単位差分をHTML化 |
| `yomogi docx2txt` | DOCXから段落テキストを抽出 |
| `yomogi kanaize` | 漢字を読みへ変換した確認用テキストを生成 |
| `yomogi kaiwa` | 会話を含む文と前後の文をMarkdownへ抽出 |
| `yomogi mora` | モーラと子音をSVG・HTMLで可視化 |
| `yomogi scenario` | シナリオテキストをHTML・DOCX化 |

詳細:

- [青空文庫](docs/aozora.md)
- [かな変換・モーラ表示](docs/mora.md)
- [シナリオ整形](docs/scenario.md)
- [その他のコマンド](docs/commands.md)

各コマンドの引数はヘルプでも確認できます。

```console
yomogi --help
yomogi mora view --help
```

## 開発

```console
python -m pip install -e .
PYTHONPATH=src pytest -q
```

## License

[MIT License](LICENSE)
