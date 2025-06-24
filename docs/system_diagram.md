# System Diagram – **Fact‑Check v1 Scope**

> **v0.9 → v1.0 スコープ整理**
> FR2（質問サジェスト）・FR3（SNS リサーチ）など **ドロップ**。Box を *薄グレー* にして将来拡張として残しています。

```mermaid
graph TD
    %% ========== スタイル定義 ==========
    classDef user fill:#f9f,stroke:#333,stroke-width:1px;
    classDef api fill:#9cf,stroke:#333,stroke-width:1px;
    classDef service fill:#6c9,stroke:#333,stroke-width:1px,color:#fff;
    classDef storage fill:#fc9,stroke:#333,stroke-width:1px;
    classDef queue fill:#f66,stroke:#333,stroke-width:1px;
    classDef model fill:#d6a6ff,stroke:#333,stroke-width:1px;
    classDef drop fill:#eee,stroke:#999,color:#666;

    %% -------------- USER --------------
    subgraph ユーザー
        User["講師 / ブラウザ"]
    end
    class User user;

    %% -------------- BACKEND --------------
    subgraph "FastAPI バックエンド"
        direction TB
        UploadAPI["Upload API"]
        FactCheckAPI["FactCheck API"]
    end
    class UploadAPI,FactCheckAPI api;

    User -->|"PPTX POST"| UploadAPI

    %% -------------- EXTRACTION --------------
    UploadAPI -->|S3保存| S3Raw["S3 PPTX 原本"]
    UploadAPI -->|抽出メッセージ| SQSExtract["extract-queue"]
    class S3Raw storage;
    class SQSExtract queue;

    subgraph "Extraction Service"
        Extractor["LibreOffice / Exparso"]
    end
    class Extractor service;

    SQSExtract --> Extractor
    Extractor -->|JSON＋PNG| S3Slide["S3 抽出データ"]
    Extractor -->|埋め込みキュー| SQSEmbed["embed-queue"]
    class S3Slide storage;
    class SQSEmbed queue;

    %% -------------- EMBEDDING --------------
    subgraph "Embedding Service"
        EmbedFn["Bedrock Titan Embeddings"]
    end
    class EmbedFn service;

    SQSEmbed --> EmbedFn
    EmbedFn -->|ベクトル保存| VectorDB["DynamoDB Vector Store"]
    class VectorDB storage;

    %% -------------- FACT CHECK --------------
    FactCheckAPI -->|RAG検索| VectorDB
    FactCheckAPI -->|照合| BedrockLLM["Bedrock LLM"]
    class BedrockLLM model;

    %% -------------- DROPPED (Future) --------------
    subgraph Future["ドロップした将来拡張"]
        QuestionSuggest["Suggest API<br/>(FR2)"]
        SNSResearch["Research API<br/>(FR3)"]
        VisionAPI["Vision API"]
        GPUGroup["GPU OSS LLM/Vision"]
    end
    %% サブグラフとノードをグレー表示
    class Future drop;
    class QuestionSuggest,SNSResearch,VisionAPI,GPUGroup drop;

    FactCheckAPI -.-> QuestionSuggest
    FactCheckAPI -.-> SNSResearch
    FactCheckAPI -.-> VisionAPI
    VisionAPI -.-> GPUGroup
```

---

## テキスト説明

| # | 処理                           | 主要サービス                         | 備考                            |
| - | ---------------------------- | ------------------------------ | ----------------------------- |
| 1 | スライド PPTX をアップロード            | **UploadAPI** (FastAPI)        | presigned URL 予定              |
| 2 | S3 に保存 & SQS 抽出キューの予定だったがAPIで直接呼出しに変更          | UploadAPI → S3Raw / SQSExtract | LocalStack で再現                |
| 3 | LibreOffice + Exparso でページ抽出 | Extraction Service             | JSON（テキスト）+ PNG を生成           |
| 4 | 埋め込み要求を SQS へ                | Extractor → SQSEmbed           |                               |
| 5 | Titan Embeddings でベクトル化      | Embedding Service              | DynamoDB VectorStore に upsert |
| 6 | ベクトル検索 (RAG)                 | FactCheckAPI                   | slide\_id + chunk で検索         |
| 7 | Bedrock LLM で真偽判定            | FactCheckAPI → Bedrock LLM     | スコア＋ハイライト返却                   |

> **グレーの Box** は *将来スコープ*（FR2, FR3, Vision, OSS GPU スタック）。
> v1.0 ではルートに含まず、コードもコメントアウト中です。

---

### 更新履歴

* **2025-06-20**: Fact‑Check 専用図に簡素化。FR2〜FR3 などはドロップ扱いとしてグレー表示 (by scope freeze)
