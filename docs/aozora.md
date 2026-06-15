# 青空文庫

図書カード番号を使って青空文庫のテキストZIPを取得し、UTF-8テキストへ変換します。

## カタログ

青空文庫公式の[公開中 作家別作品一覧拡充版（UTF-8、ZIP圧縮）](https://www.aozora.gr.jp/index_pages/list_person_all_extended_utf8.zip)をダウンロードして展開し、CSVを次の場所へ配置します。

```text
data/aozora/list_person_all_extended_utf8.csv
```

別の場所に置く場合は`--catalog`で指定できます。

## 取得

図書カード番号を指定します。たとえば、図書カードのURLが
`https://www.aozora.gr.jp/cards/000148/card4088.html`の場合、番号は`4088`です。

```console
yomogi aozora fetch 4088
```

この番号をCSVの`作品ID`列から検索し、カタログ内のテキストURLから次の2ファイルを生成します。

```text
4088_ruby_5542.zip
4088_ruby_5542.org.txt
```

`.org.txt`はZIP内のテキストを展開し、UTF-8へ変換した未加工テキストです。

出力するZIP名を指定する場合:

```console
yomogi aozora fetch 4088 -o downloads/4088.zip
```

## 整形

```console
yomogi aozora extract 4088_ruby_5542.org.txt
```

次の処理を行い、`4088_ruby_5542.txt`を生成します。

- 冒頭の記号説明ブロックを除去
- 末尾の底本情報と青空文庫定型文を除去
- ルビ記号を除去
- 対応済みの`［＃...］`注記を変換

未対応の注記は削除せず、警告を表示してテキスト内に残します。

## 注記の変換規則

`［＃...］`注記の変換規則は
[src/yomogi/commands/aozora/annotations.py](../src/yomogi/commands/aozora/annotations.py)
に定義しています。

- 外字などの個別変換は`EXACT_REPLACEMENTS`
- 字下げは`INDENT_PATTERN`
- 見出し、改ページ、傍点などの除去は`REMOVE_PATTERNS`

未対応の注記を追加するときは、このファイルへ変換規則を追加します。
