# JsonToPlist
JSON から Plist へ変換するツールです。

## 使用方法

	json2plist.py [-h] [--ext [EXT]] filename [filename ...]

* -h: ヘルプを表示します。
* --ext 拡張子: 出力ファイルの拡張子を指定します。
* filename: ファイル名です。

## 使用例

hoge.json → hoge.plist の変換を行う

	json2plist.py hoge.json

hoge.json → hoge.plist, fuga.json → fuga.plist の変換を行う

	json2plist.py hoge.json fuga.json

hoge.json → hoge.xml の変換を行う

	json2plist.py --ext xml hoge.json
