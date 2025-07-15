## 使い方メモ

### ローカルMCP

1. デバッグしたいMCPサーバディレクトリまで移動
2. 以下を実行
npx @modelcontextprotocol/inspector uv run {起動したいファイル名}
例：npx @modelcontextprotocol/inspector uv run weather.py
3. セッショントークン額踏まれるURLが発行されるので選択。
4. Toolsに作成した機能がリスト表示されるので、適当に選んで実行することで返り値のJSON含め正しく動くか確認できる。