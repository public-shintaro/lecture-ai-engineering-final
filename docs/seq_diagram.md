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
![alt text](image-1.png)
> **ポイント**
>
> * **Upload API** と **Extraction API** の両方を明示。開発環境では Extraction API に直接 POST して抽出を確認できます。
> * 本番では Upload API ➜ S3 ➜ SQS ➜ Extraction Worker の非同期ルートを使用します。
> * Embedding Service まで含め、ベクトルが DynamoDB に保存されるところまで記載しています。

---

## Sequence Diagram – FactCheck (v1 scope)

```mermaid
sequenceDiagram
    title FactCheck API シーケンス

    participant User as ブラウザ利用者
    participant FactCheckAPI as FactCheck API (/factcheck)
    participant DynamoDB as DynamoDB VectorStore
    participant BedrockLLM as Bedrock LLM

    User ->>+ FactCheckAPI: 1. POST /factcheck (slide_id)
    FactCheckAPI ->> DynamoDB: 2. Query (top‑k chunks)
    DynamoDB -->> FactCheckAPI: 3. チャンク集合
    FactCheckAPI ->> BedrockLLM: 4. Prompt with retrieved context
    BedrockLLM -->> FactCheckAPI: 5. Verdict (score, citation)
    FactCheckAPI -->>- User: 6. JSON result (highlights, score)
```
![alt text](image-2.png)