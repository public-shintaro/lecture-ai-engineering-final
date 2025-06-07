# 講義AIエンジニアリング 最終課題プロジェクト

このプロジェクトは、講義スライドをAIでファクトチェックし、補足情報を提供することで、教育コンテンツの品質を向上させることを目的としています。

---

## 🚀 Quick Start

開発環境を迅速に立ち上げるための手順です。VS CodeとDev Container拡張機能を使用していることを前提とします。

### 1. 開発環境の起動

1.  このリポジトリをクローンします。
2.  VS Codeでリポジトリのフォルダを開きます。
3.  VS CodeがDev Containerでの再オープンを推奨する通知を表示しますので、「Reopen in Container」をクリックします。
4.  初回はコンテナのビルドに時間がかかります。ビルドが完了すると、開発に必要なツールがすべて含まれた環境が起動します。

### 2. 全サービスの起動

Dev Container内のターミナルで以下のコマンドを実行します。これにより、必要なすべてのサービス（Extraction API, MLflow UI）が起動します。

```bash
docker compose -f docker-compose.dev.yml up --build -d

### 3. 停止方法

以下のコマンドで、起動しているすべてのコンテナを停止・削除します。

docker compose -f docker-compose.dev.yml down

### 4. サービス URL と利用方法

サービス起動後、以下のURLにアクセスできます。

- Extraction API (Swagger UI):
  Windows/Macのブラウザから: http://localhost:8080/docs
- MLflow UI:
  Windows/Macのブラウザから: http://localhost:5000

サンプルAPI実行例

Dev Container内のターミナルから、extractionサービスにサンプルPPTXファイルを送信して動作を確認します。

# プロジェクトのルートディレクトリで実行
curl -X POST -F "file=@tests/test_sample.pptx" http://extraction:8080/extract
