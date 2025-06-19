日本語で会話してください。ただしcommitメッセージとかは英語でお願いします。

## 概要

AIエンジニアリング実践講座（AIE2504) 最終課題.mdの内容に従って、AIエンジニアリング実践講座の最終課題を実装します。

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
- Add a comment at the end of the file: 'Contains some AI-generated edits.'


## 開発カレンダー（6 / 3 – 7 / 6 , 1 日あたり **3 h** を基本）

*MVP＝Bedrock 版を 6 / 22 に完成 ⇒ その後ストレッチで OSS‐GPU (ECS/Fargate) 版を 7 / 6 までに実装*

| 日付 | フェーズ | タスク (│=並行可) | 期待アウトプット |
|------|---------|------------------|------------------|
| **6/3 火** | 計画 / 環境 | キックオフ ─ 要件・Bedrock 方針最終確認 │ GitHub リポジトリ初期化 │ Dev コンテナ作成 | リポジトリ & 開発環境 |
| **6/4 水** | 環境 | CI 雛形 (GitHub Actions) │ Exparso 抽出テスト | pytest tests/test_exparso_pptx.py でサンプル PPTX を解析し JSON が返ることを確認 |
| **6/5 木** | 環境 | 抽出サービス Docker 化 │ MLflow local 起動 | 抽出 image & MLflow URL |
| **6/6 金** | 抽出 / Embed | **Exparso 導入 & `parse_pptx()` PoC │ Titan Embeddings v2 API 組込み │ DynamoDB+自力サーチ(cos類似度) 作成** | `/embed` 完了 |
| **6/7 土** | Bedrock | **Bedrock Vision (Claude 3 Image) 連携 │ スライド JSON 拡充** | `/vision` API |
| **6/8 日** | **バッファ** | （遅延吸収 or 追加微調整） |  |
| **6/9 月** | アルゴ | RAG ファクトチェック関数 │ Precision/Recall notebook | 不整合 JSON |
| **6/10 火** | 画像 | （6/7 で完了済につきタスク軽減） | — |
| **6/11 水** | BE | FastAPI スケルトン │ `/api/upload` | Upload 動作 |
| **6/12 木** | BE | factcheck Router (Bedrock) │ DynamoDB 統合 | `/api/factcheck` |
| **6/13 金** | BE | suggest Router (Bedrock) │ APA citation 関数 | `/api/suggest` |
| **6/14 土** | BE | feedback Router & DB │ LLM-Judge プロンプト (Bedrock) | `/api/feedback` |
| **6/14 (土)** | **BE**     | **Step 8:** `aioboto3` で S3 保存／SQS Publish │ LocalStack で結合テスト  | `/api/upload` が S3 & SQS 動作 |
| **6/15 (日)** | BE         | 抽出サービスを **S3 + SQS** 対応 (ダウンロード→チャンク化) │ embed\_service 呼び出しモック | 抽出ジョブ完走 & VectorDB upsert   |
| **6/17 (火)** | BE         | `/api/factcheck` ルーター │ DynamoDB 結合 │ Bedrock 呼び出し           | `/api/factcheck` 返却 JSON    |

## リカバリー計画 <factckeckの実装>
| 日付           | 主テーマ (3h)               | 具体的な完了基準                                                                                                                                                                                             |
| ------------ | ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **6/20 (金)** | **スコープ凍結 & 既存タスク整理**    | \* FR2〜FR4 に関わるコード／CIステップをコメントアウトまたは削除<br>\* `README.md`・`docs/system_diagram.md` を Fact-Check 専用構成に更新<br>\* GitHub Projects ボードを本表に合わせて再編                                                           |
| **6/21 (土)** | **CI / 静的解析をグリーンに**     | \* `vector_store.get_chunks_by_document_id` の `Optional` 対応で **mypy** エラー解消<br>\* `.github/workflows/ci.yml` に LibreOffice (headless) インストール追加<br>\* GitHub Actions で **pytest / Ruff / mypy** すべてパス |
| **6/22 (日)** | **抽出 → S3 → SQS の堅牢化**  | \* PPTX → チャンク → S3 保存 & SQS メッセージ生成を LocalStack/AWS で検証<br>\* `tests/test_extraction_e2e.py` を追加し CI で自動確認                                                                                          |
| **6/23 (月)** | **embed\_service 最小実装** | \* Bedrock Titan もしくは Sentence-Transformers で埋め込み生成 API を実装<br>\* ベクトルを Faiss (dev)／DynamoDB (prod想定) に格納<br>\* `mlflow.log_model` でモデル版管理                                                           |
| **6/24 (火)** | **SQS コンシューマ実装**        | \* embed\_service に非同期バックグラウンドワーカーを追加し SQS 受信 → ベクトル upsert<br>\* 「PPTX アップロード ➜ ベクトル行が DB に追加」まで E2E で通る                                                                                            |
| **6/25 (水)** | **Fact-Check コア実装**     | \* `factcheck.py` で RAG 取得＋LLM 照合ロジックを完成<br>\* 信頼度スコア・ハイライト位置を返すスキーマ確定                                                                                                                               |
| **6/26 (木)** | **評価ハーネス & メトリクス**      | \* `scripts/eval_factcheck.py` で precision / recall を計算<br>\* `data/ground_truth/` と突き合わせて **top-5 precision ≥ 60 %** 達成                                                                             |
| **6/27 (金)** | **サービス統合テスト**           | \* `pytest -m "e2e"` で docker-compose.dev を立ち上げ、抽出→埋込→Fact-Check を一括テスト                                                                                                                              |
| **6/28 (土)** | **AWS へデプロイ (開発環境)**    | \* Docker イメージを ECR へ push<br>\* ECS Fargate または Lambda/API Gateway で最短ルートのデプロイ<br>\* 公開 URL で Smoke Test 成功                                                                                         |
| **6/29 (日)** | **レポート & デモ動画草稿**       | \* スライドにアーキ・ドライバ・評価結果・スクリーンショットを整理<br>\* OBS などで 3 分程度のデモ録画                                                                                                                                          |
| **6/30 (月)** | **仕上げ & 予備日**           | \* バグ取り・ドキュメント最終チェック・README 完全版<br>\* `v1.0` タグ付け＆提出                                                                                                                                                 |

## ストレッチ〈LoRA 最小ファインチューニング & OSS 実行〉

| 日付          | 重点テーマ                   | 具体的タスク & 成果物                                                                                                                                                                                |
| ----------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **7/1 (火)** | **OSS 下調べ & データ整備**     | \* Fact-Check 向けに最小 LoRA が可能な OSS（`peft`, `unsloth`, `qlora`, `lora-scripts` など）を比較し 1 つ決定<br>\* `data/ground_truth/` を学習フォーマット（Alpaca-JSON）へ変換するスクリプト `scripts/prepare_lora_dataset.py` 作成 |
| **7/2 (水)** | **環境セットアップ & 学習ジョブ開始**  | \* Dockerfile（`docker/lora_train.Dockerfile`）で CUDA / bitsandbytes / peft をインストール<br>\* `scripts/run_lora_train.sh` を用意し **TinyLlama-1.1B** など軽量モデルで学習をキック<br>\* MLflow 追跡を有効化              |
| **7/3 (木)** | **モデル登録 & 推論 API 試作**   | \* 学習済み LoRA アダプタを `mlflow.log_model` → `models/lora_factcheck/` に登録<br>\* `factcheck_service/routers/lora_predict.py` を仮追加し、既存 LLM 呼び出しと差し替え可能に                                            |
| **7/4 (金)** | **評価 & ベンチマーク**         | \* `scripts/eval_factcheck.py --model lora` で Precision / Recall を再計測し、baseline と比較<br>\* 目標: **top-5 precision +5 pt** 以上の改善                                                               |
| **7/5 (土)** | **推論最適化 & コンテナ化**       | \* `auto_gptq` or `bitsandbytes-int4` で量子化 → 速度／VRAM を測定<br>\* `docker/lora_inference.Dockerfile` を作成し ECS/Lambda で動くイメージをビルド                                                               |
| **7/6 (日)** | **ドキュメンテーション & 最終チェック** | \* README に “LoRA 最小構成手順” 追記、`docs/lora_report.md` に目的・手順・結果をまとめる<br>\* GitHub Release `v1.1-lora` タグ、CI で学習・評価ジョブが通ることを確認                                                                  |
