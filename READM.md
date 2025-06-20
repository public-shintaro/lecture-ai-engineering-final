# 講義 AI エンジニアリング ★ 最終課題

PowerPoint 形式の講義スライドを **AI でファクトチェック (FR1)** するサンプルアプリです。

* 💡 *FR2（質問サジェスト）/FR3（SNS リサーチ）などは現在スコープ外*
* AWS を完全エミュレートする **LocalStack** と **MLflow** を含む **Docker‑Compose** で再現性の高い開発環境を提供します。

---

## 🚀 Quick Start（VS Code Dev Container）

```
├─ .devcontainer/               # VS Code 開発用イメージ
├─ backend/
│   ├─ app/                     # FastAPI 共通設定・依存注入
│   ├─ services/                # 業務ロジック層（将来機能拡張用）
│   ├─ extraction_service/
│   │   └─ app/                 # Extraction API エントリポイント
│   ├─ upload_service/          # ファイル受取 API (Next.js UIと連携予定)
│   └─ ...
├─ docker-compose.dev.yml       # 開発用サービス定義
├─ tests/                       # pytest + LocalStack
└─ scripts/                     # init_localstack.sh 等の補助スクリプト
```

````

---

## ⚙️ GitHub Actions / CI

- `.github/workflows/ci.yml` で **pytest / mypy / Ruff** を実行。
- CI 内でも **docker-compose.dev.yml** を起動し、LocalStack + MLflow を再現します。
- LibreOffice (headless) をインストールして PPTX 解析をテストします。

---

## 🏷️ 環境変数 (.env 例)

```dotenv
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=dummy
AWS_SECRET_ACCESS_KEY=dummy
AWS_ENDPOINT_URL=http://localstack:4566
UPLOAD_BUCKET=lecture-slide-files
EXTRACT_QUEUE_NAME=slide-extract-queue
EXTRACT_QUEUE_URL=http://localstack:4566/000000000000/slide-extract-queue
VECTOR_TABLE_NAME=lecture-vector-store-dev
MLFLOW_TRACKING_URI=http://mlflow:5000
````

---

## 🐞 トラブルシューティング

| 症状                                       | 原因 & 解決                                             |
| ---------------------------------------- | --------------------------------------------------- |
| ブラウザで `http://localhost:8000/docs` が開けない | compose マッピングを確認 (`8000:8080`)。`docker ps` でポートを要確認 |
| CI で "Connection refused"                | テスト中の URL が `localhost` になっていないか確認。サービス名でアクセスする     |
| LocalStack のリソースが空っぽ                     | `scripts/init_localstack.sh` が完走しているか logs を確認      |

---

## 📜 ライセンス

このリポジトリは MIT License です。

---
