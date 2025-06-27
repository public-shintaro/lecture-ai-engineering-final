# Sequence Diagram – Upload & Extraction (v1 scope)

```mermaid
sequenceDiagram
    title ファイルアップロード & Extraction Service のシーケンス

    %%====== Actors ======
    participant User as ブラウザ利用者
    participant UploadAPI as Upload API (/upload)
    participant S3Raw as S3 PPTX原本
    participant SQSExtract as SQS extract-queue
    participant ExtractionWorker as Extraction Worker
    participant ExtractionAPI as Extraction API (/extract)
    participant S3Slide as S3 抽出データ
    participant SQSEmbed as SQS embed-queue
    participant EmbedSvc as Embedding Service
    participant DynamoDB as DynamoDB VectorStore

    %%====== Primary (Prod) Flow ======
    User ->>+ UploadAPI: 1. POST /upload (PPTX, slide_id)
    UploadAPI ->> S3Raw: 2. putObject (PPTX)
    UploadAPI ->> SQSExtract: 3. SendMessage (slide_id, S3 key)
    UploadAPI -->>- User: 4. HTTP 202 Accepted

    %% async
    ExtractionWorker ->>+ SQSExtract: 5. Poll for message
    SQSExtract -->>- ExtractionWorker: 6. ReceiveMessage
    ExtractionWorker ->> S3Raw: 7. getObject (PPTX)
    ExtractionWorker ->>+ ExtractionAPI: 8. POST /extract (binary)
    ExtractionAPI -->>- ExtractionWorker: 9. JSON chunks & PNG

    ExtractionWorker ->> S3Slide: 10. putObject (chunk JSON / PNG)
    ExtractionWorker ->> SQSEmbed: 11. SendMessage (chunk metadata)
    ExtractionWorker ->>+ SQSExtract: 12. DeleteMessage
    SQSExtract -->>- ExtractionWorker: 13. OK

    %% Embedding
    EmbedSvc ->>+ SQSEmbed: 14. Poll for chunk
    SQSEmbed -->>- EmbedSvc: 15. ReceiveMessage
    EmbedSvc ->> DynamoDB: 16. BatchWriteItem (vector rows)
    EmbedSvc ->>+ SQSEmbed: 17. DeleteMessage
    SQSEmbed -->>- EmbedSvc: 18. OK

    Note over User, DynamoDB: これでベクトルDBにチャンクが保存され、FactCheck API から検索可能になる。

    %%====== Dev Shortcut (直接抽出) ======
    alt 開発／ローカル動作
        User ->>+ ExtractionAPI: A1. POST /extract (PPTX)
        ExtractionAPI -->>- User: A2. JSON chunks & PNG (同期)
    end
```
> **ポイント**
>
> * **Upload API** と **Extraction API** の両方を明示。開発環境では Extraction API に直接 POST して抽出を確認できます。
> * 本番では Upload API ➜ S3 ➜ SQS ➜ Extraction Worker の非同期ルートを使用します。
> * Embedding Service まで含め、ベクトルが DynamoDB に保存されるところまで記載しています。

---
# Sequence Diagram – Upload & Extraction (v1.1 scope)

```mermaid
sequenceDiagram
    autonumber
    participant Browser          as ブラウザ利用者
    participant UploadAPI        as Upload API<br/>(FastAPI :8000)
    participant S3raw            as S3 PPTX原本
    participant Extraction       as Extraction Service<br/>(FastAPI :8080)
    participant S3chunks         as S3 チャンク保存
    participant Titan            as Bedrock Titan
    participant DDB              as DynamoDB slide_chunks

    Browser  ->> UploadAPI : 1. POST /upload (file, slide_id)
    UploadAPI ->> S3raw    : 2. putObject(PPTX)
    UploadAPI ->> Extraction: 3. POST /extract (binary body)
    Extraction ->> S3chunks: 4. putObject(chunk_###.txt)*
    Extraction -->> UploadAPI: 5. JSON [{"idx":0,"s3_key":…}, …]

    %% ─── ここまで 1〜6 は従来どおり ───
    loop 各 chunk
        UploadAPI ->> S3chunks: 6. getObject(chunk_###.txt)
        %% 変更点 : Step7 は Extraction Service へ送る
        UploadAPI ->> Extraction: 7. POST /embed (text, slide_id, idx)
        %% 以下 8–10 は Extraction Service 内部処理
        Extraction ->> Titan: 8. invoke_model(text)
        Titan -->> Extraction: 9. embedding[1536]
        Extraction ->> DDB: 10. putItem(PK=slide_id#idx, embedding)
        Extraction -->> UploadAPI: 11. OK
    end

    UploadAPI -->> Browser: 12. HTTP 200 OK {"chunks": N}

```

## Sequence Diagram – FactCheck (v1 scope)

```mermaid
sequenceDiagram
    title: FactCheck API (v1) – ページ単位＆スライド全体の流れ

    %% ─── 登場人物 ───────────────────────────────────────
    participant U   as ユーザー／フロントエンド
    participant API as FactCheck API<br/>(FastAPI `/factcheck`)
    participant VS  as Vector Store<br/>(DynamoDB など)
    participant LLM as Bedrock Claude 3 Sonnet

    %% ─── 1. リクエスト ────────────────────────────────
    U ->>+ API: POST `/factcheck` { slide_id, pages? }

    Note right of API: `pages` 省略時は\nスライド内の全ページ番号を取得

    %% ─── 2. ページごとの証拠取得＆検証 ───────────────
    loop 各 page ∈ PAGES
        API  ->> VS  : query(<slide_id, page>) → 上位チャンク
        VS   -->> API: チャンク内容（テキスト＋メタデータ）

        API  ->> LLM : 「page {{page}} をファクトチェック」＋コンテキスト
        LLM  -->> API: verdict, issues[], citations[]

        API  ->> API : per_page_results に追加
    end

    %% ─── 3. スライド全体サマリ（任意） ───────────────
    alt PAGES.length > 1
        API ->> LLM : 「スライド全体を総括」＋ per_page_results
        LLM -->> API: slide_summary
    end

    %% ─── 4. レスポンス ───────────────────────────────
    API -->>- U : 200 OK JSON\n{ per_page_results, slide_summary? }
```
