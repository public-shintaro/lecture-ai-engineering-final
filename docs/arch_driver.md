| **カテゴリ** | **アーキテクチャドライバ** | **説明・根拠** |
|--------------|---------------------------|----------------|
| **機能要件** | **FR1. 講義スライドのファクトチェック [必須]** | **Exparso (OSS) が LibreOffice を内部呼び出しして PPTX → 構造化 JSON / PNG を抽出。**<br>得られたテキスト・表・画像を **Titan Embeddings v2 (Bedrock)** でベクトル化し OpenSearch Serverless に登録。Bedrock Claude 3（LLM）＋Claude 3 Image API で RAG し、矛盾・出典なし箇所をハイライト表示。 |
|              | **FR2. 質問・補足情報サジェスト [必須]** | Claude 3 (Bedrock) で想定質問／不足背景を生成。画像は **Claude 3 Image API**（または Rekognition＋Titan）でキャプション化し、メタ検索＋画像検索で出典を取得し APA 形式で提示。 |
|              | **FR3. 関連最新情報リサーチ [任意]** | 無料 API／RSS で SNS・技術サイトを収集し、投稿数・ポジネガ・論点を分析 |
|              | **FR4. 多言語対応（日・英） [必須]** | ja/en 自動判定し **MVP は Titan Embeddings v2**、Stretch で `bge-ja` / `gte-base`（CPU）に切替可 |
|              | **FR5. PDF インサイトレポート生成 [ストレッチ]** | FR3 が実装できた場合に、PNG グラフを自動レイアウトし A4 PDF を生成（6 / 23–6 / 28 のバッファで対応） |
|              | **FR6. フィードバック収集 & 質評価 [必須]** | **Claude 3 (Bedrock) を Judge** として ☆1–5 + コメントを取得しモデル改善とレポートに反映 |
| **品質特性** | **QA1. コスト効率** | Bedrock（Claude 3・Titan 系）+ 無料 API で **開発期間中** の AWS コスト/月 ≤ 200 USD（GPU/OSS ルートは Stretch で追加） |
|              | **QA2. パフォーマンス** | FR2：アップロード後 ≤ 2 s で初期結果、FR1/FR3：全処理 ≤ 10 min |
|              | **QA3. ユーザビリティ** | Web UI のサムネイルにハイライト、差分は WebSocket で即時更新 |
|              | **QA4. 拡張性** | **今期はモジュール性の高い設計**を優先し、将来マイクロサービス化を容易に |
|              | **QA5. 開発・運用効率** | MLflow + IaC + GitHub Actions で再現性と自動化を確保 |
|              | **QA6. 観測性・テスト容易性** | PyTest は必須、OpenTelemetry・Grafana・k6 は **ストレッチゴール** |
|              | **QA7. 提示情報の品質** | KPI: Precision ≥ 0.80 / Recall ≥ 0.70、サジェスト有用率 ≥ 70 % |
| **制約条件** | **C1. 短期開発** | 6 / 2–6 / 22、1 日 3 h（計 ≈ 63 h）。最優先は **FR1 + FR2** を備えた Bedrock Web MVP；6 / 23 以降をバッファ |
|              | **C2. OSS モデルをストレッチゴールで利用** | RTX 5080 と AWS g5.xlarge で動作。GPU コンテナ（Gemma / LLaVA）は **7 / 6 までの Stretch** で実装 |
|              | **C3. 対象ユーザー** | 主利用者＝講師 |
|              | **C4. 提供形態** | MVP＝Web サービス；PowerPoint アドインはストレッチ |
|              | **C5. データプライバシ & セキュリティ** | PoC：S3 限定公開＋最小権限 IAM、追加要件なし |
|              | **C6. プラットフォーム** | 既存 AWS アカウント／MLflow サーバ (ECS/Fargate) |
|              | **C7. ライセンス & 無料 API** | Apache-2.0（Exparso）／MIT/BSD ライブラリ；X (旧Twitter) は無料枠で取得可能な範囲に限定 |
|              | **C8. ファイル形式限定** | 入出力 PPTX；抽出は **Exparso (LibreOffice 内部依存) → JSON/PNG**。LibreOffice コンテナは Batch で自動利用し、追加実装コストを最小化 |
Contains AI-generated edits.
