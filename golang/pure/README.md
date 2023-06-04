# Golang - Pure
Go言語にデフォルトで入っている`http`パッケージを利用したAPIサーバー。

## Installation
1. 以下のコマンドを実行する。
    
    ```shell
    cd golang/pure
    ```

2. カレントディレクトリをVSCodeのDev Containersで開く。
3. 以下のコマンドを実行する（docker-compose.ymlに含めたい）。

    ```shell
    go install -v golang.org/x/tools/gopls@latest
    ```


## Getting Started
- 以下のコマンドを実行して、APIサーバーを起動する。

    ```shell
    go run main.go
    ```
