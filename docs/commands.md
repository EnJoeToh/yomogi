# その他のコマンド

## diff

2つのUTF-8テキストを比較し、語単位の差分HTMLを生成します。

```console
yomogi diff old.txt new.txt
```

既定の出力:

```text
new.diff.html
```

横書きにする場合:

```console
yomogi diff old.txt new.txt --layout horizontal
```

## docx2txt

DOCXの段落テキストを抽出します。

```console
yomogi docx2txt input.docx -o output.txt
```

`-o`を省略すると標準出力へ表示します。

## kaiwa

`「...」`を含む文と、その前後の文をMarkdownへ抽出します。

```console
yomogi kaiwa novel.txt
```

既定の出力:

```text
novel.kaiwa.md
```
