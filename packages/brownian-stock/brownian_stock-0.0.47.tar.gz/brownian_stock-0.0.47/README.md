

# Brownian
[![Python application](https://github.com/toritoritori29/brownian/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/toritoritori29/brownian/actions/workflows/python-app.yml)

Brownianは日本株取引に対応した株取引フレームワークです。JQuantsからのデータダウンロード, 取引モデルの作成, バックテスト, 実取引まで網羅的にサポートします.


## Usage


以下のサブコマンドを実行すると指定したディレクトリ以下にJQuantesから取得した情報をCSVで保存します. 
```
brownian download <保存先のディレクトリ名>
```

### ログイン情報の設定
またdownloadオプションには`--username`および`--password`オプションが用意されていて、実行時にこれらの引数を指定して実行することもできます。
これらの引数は.brownianrcの内容より優先して利用されます。

## DBの更新・CSVの生成
以下のコマンドを実行すると, ダウンロードしたデータを集計してSQLiteデータベース上に格納します.
またデータベースから銘柄毎の株価情報・決算情報を集計しCSVを生成します. 

```
$ brownian download <保存先フォルダ名>
$ brownian generate <保存先フォルダ名>
```

## ディレクトリの構成

### raw_stock
JQuantsから取得した日毎の株価情報

### raw_statements
JQuantsから取得した日毎の決算情報

## stock
`genereate`コマンドで生成した銘柄毎の株価情報.　株価は調整済みの数字.

## Install

各種コマンドのインストール前にvenvをactivateしてください.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

# For Developer

## Prerequires
* pyenv
* poetry == 1.4.2
* gh

## Set up
Run following commands.
```
pyenv install -s 3.10.4 && poetry env use 3.10.4
poetry install 
```

## Utility commands.

* To test.
```
poetry run pytest
```

* Lint and format
```
poetry run invoke lint
poetry run invoke format
```

