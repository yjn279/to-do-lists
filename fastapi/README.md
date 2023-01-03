# FastAPI

## Requirements
以下のコマンドを実行して環境を構築する。
```
python3 -m venv venv
pip install --upgreade pip
pip install poetry
poetry install 
```

`.env.sample`ファイルにならって`.env`ファイルを作成する。
`SECRET_KEY`は以下のコマンドで生成できる。
```
openssl rand -hex 32
```


## Getting started
サーバーの起動
```
poetry run task dev
```

Lint & Format
```
poetry run task check
```
