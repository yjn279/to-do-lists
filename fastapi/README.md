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

OpenAPI ドキュメント
http://127.0.0.1:8000/docs

## References
- [FastAPI](https://fastapi.tiangolo.com/ja/)
- [FastAPIを勉強する](https://zenn.dev/yuji207/scraps/4ab2fdb73ae232)
