日本語で会話してください。ただしcommitメッセージとかは英語でお願いします。

## 概要

C:\Users\0000100142\OneDrive - Sony\src\lecture-ai-engineering-final\docs\AIエンジニアリング実践講座（AIE2504) 最終課題.md
の内容に従って、AIエンジニアリング実践講座の最終課題を実装します。

## 設計原則
- DRY:"Don't Repeat Yourself"の略。同じコードを重複させず、一箇所にまとめるという原則
- KISS:"Keep It Simple, Stupid"の略。コードはできるだけシンプルにすべきという原則
- YAGNI:"You Aren't Gonna Need It"の略。「今必要な機能‧コード以外は書かない」という原則
- Do NOT Over Engineering/ビルドトラップがある
    § 精度100%を目指してしまう
    § 基盤モデルを使う際に必要以上に高性能なモデルを使ってしまう
    § ユーザー数が少ない社内システムで秒間数万アクセスに耐えられるアーキテクチャを構築してしまう
    § ユーザーではないステークホルダーの声を聞いて不要な機能を作ってしまう
    § 使われていない機能を残し続けてしまう

## Workflow
ghコマンドを使って下記を実践します。
- ghコマンドでissueを作成します。
- issueを見て、実装する内容を決めます。
- GitHub Flowを採用します。ghコマンドでpull requestを作成します。
- pull requestを作成したら、レビューを依頼します。
- レビューが通ったら、マージします。
- マージしたら、ghコマンドでissueをクローズします。

## 開発環境
- 開発環境は、Dev Containerを使って構築します。
- Dev Containerは、Dockerを使って構築します。
- 開発環境は、Pythonを使って構築します。
- リポジトリはモノレポジトリでフロントエンドとバックエンドを分けて実装します。
- フロントエンドは、Next.jsを使って実装します。
- バックエンドは、FastAPIを使って実装します。
- バックエンドは、Python 3.11を使って実装します。
- バックエンドは、[AWSを使います](./docs/system_diagram.md)。

## テスト

- ユニットテストを必ず書いてください(TDDの原則に従う)
- GitHub Actionsを使ってCI/CDを実装します。
- CI/CDの実装は、GitHub Actionsを使って自動化します。

## コーディングガイドライン

Apply the [general coding guidelines](https://google.github.io/styleguide/) to all code you generate.

- 必ず英語でわかりやすいようにコメントを英語で入れてください
- docs/以下のファイルは実装の内容が変わったら一緒に必ず修正してください
- docs/以下のファイルは内容が変わるような実装は必ず私に許可を得てください。
- Add a comment at the end of the file: 'Contains AI-generated edits.'


## 開発カレンダー（6 / 3 – 7 / 6 , 1 日あたり **3 h** を基本）  

*MVP＝Bedrock 版を 6 / 22 に完成 ⇒ その後ストレッチで OSS‐GPU (ECS/Fargate) 版を 7 / 6 までに実装*

| 日付 | フェーズ | タスク (│=並行可) | 期待アウトプット |
|------|---------|------------------|------------------|
| **6/3 火** | 計画 / 環境 | キックオフ ─ 要件・Bedrock 方針最終確認 │ GitHub リポジトリ初期化 │ Dev コンテナ作成 | リポジトリ & 開発環境 |
| **6/4 水** | 環境 | CI 雛形 (GitHub Actions) │ `python-pptx`／`unoconv` 検証 | 抽出 PoC |
| **6/5 木** | 環境 | 抽出サービス Docker 化 │ MLflow local 起動 | 抽出 image & MLflow URL |
| **6/6 金** | 抽出 / Embed | **Exparso 導入 & `parse_pptx()` PoC │ Titan Embeddings v2 API 組込み │ OpenSearch Serverless 作成** | `/embed` 完了 |
| **6/7 土** | Bedrock | **Bedrock Vision (Claude 3 Image) 連携 │ スライド JSON 拡充** | `/vision` API |
| **6/8 日** | **バッファ** | （遅延吸収 or 追加微調整） |  |
| **6/9 月** | アルゴ | RAG ファクトチェック関数 │ Precision/Recall notebook | 不整合 JSON |
| **6/10 火** | 画像 | （6/7 で完了済につきタスク軽減） | — |
| **6/11 水** | BE | FastAPI スケルトン │ `/api/upload` | Upload 動作 |
| **6/12 木** | BE | factcheck Router (Bedrock) │ OpenSearch 統合 | `/api/factcheck` |
| **6/13 金** | BE | suggest Router (Bedrock) │ APA citation 関数 | `/api/suggest` |
| **6/14 土** | BE | feedback Router & DB │ LLM-Judge プロンプト (Bedrock) | `/api/feedback` |
| **6/15 日** | FE | Next.js アップロード UI │ WebSocket 基盤 | アップロード UI |
| **6/16 月** | FE | スライドサムネイル + ハイライト描画 | ハイライト表示 |
| **6/17 火** | FE | Q&A / citation パネル │ コピー機能 | 情報パネル |
| **6/18 水** | FE | フィードバック UI（星 + コメント） | 評価送信可 |
| **6/19 木** | テスト | PyTest 単体 / 結合 │ CI 緑化 |  |
| **6/20 金** | **フリー バッファ** | KPI 計測前倒し・遅延調整 |  |
| **6/21 土** | ドキュメント | README / Runbook │ アーキ図整備 | docs v0.9 |
| **6/22 日** | **Bedrock MVP 提出** | デモ動画収録・編集 │ 最終レポート仕上げ | MVP 提出一式 |

#### ── Stretch フェーズ：OSS-GPU (ECS) ＋ FR3/FR5 ──

| 日付 | フェーズ | タスク | 期待アウトプット |
|------|---------|--------|------------------|
| **6/23 月** | GPU 基盤 | vLLM コンテナ (`gemma-3`) ビルド │ ECR push | `llm:v1` |
| **6/24 火** | GPU 基盤 | LLaVA-NeXT コンテナ ビルド │ ECR push | `vision:v1` |
| **6/25 水** | インフラ | ECS Cluster + Fargate GPU (g5.xl) │ ALB 作成 | GPU サービス起動 |
| **6/26 木** | BE 切替 | FastAPI ルーターを **FeatureFlag** で OSS / Bedrock 切替可に | `/api/*` dual-path |
| **6/27 金** | Embed 切替 | LambdaEmbed → bge/​gte (CPU) │ OpenSearch 書込み確認 | OSS ルート完成 |
| **6/28 土** | **FR3 収集基盤** | RSS / X / Qiita クローラ │ `/crawl` バッチ | VectorDB 追加 |
| **6/29 日** | **FR3 解析** | ポジネガ判定 │ キーフレーズ抽出 | `/analyze` |
| **6/30 月** | **FR5 PDF** | Matplotlib グラフ │ `reportlab` PDF 組版 | Insight PDF |
| **7/1 火** | 観測 | OpenTelemetry exporter │ Grafana Dashboard | Dash v0.1 |
| **7/2 水** | 負荷試験 | k6 シナリオ作成 │ GPU / Bedrock 両ルート測定 | レイテンシ報告 |
| **7/3 木** | LoRA (任意) | Gemma LoRA fine-tune (RTX 5080 夜間) | LoRA ckpt |
| **7/4 金** | コスト最適 | Auto-pause OpenSearch PoC │ GPU Auto-scale Lambda | 料金レポート |
| **7/5 土** | 仕上げ | README/​docs 更新 │ Demo 追撮 │ バグ修正 | Stretch docs |
| **7/6 日** | **Stretch 提出** | 最終デモ動画（OSS 比較含む）│ レポート追補 | Stretch 提出一式 |
