graph TD
    %% ─── ユーザー ──────────────────────────────
    subgraph "ユーザー"
        User["講師"] -- "interacts via browser" --> FE["Next.js フロントエンド"]
    end

    %% ─── AWS クラウド ───────────────────────────
    subgraph "AWSクラウド環境 (VPC 内)"
        FE -- "HTTPS API Calls" --> APIGW["API Gateway"]

        %% ── 軽量サーバーレス API
        subgraph "サーバーレス API (軽量処理)"
            APIGW -- "/upload" --> LambdaUpload["AWS Lambda: Upload Router"]
            APIGW -- "/feedback" --> LambdaFeedback["AWS Lambda: Feedback Router"]
        end

        %% ── AI 推論レイヤ ①：Bedrock (MVP – 実線)
        subgraph "Bedrock マネージド AI (MVP 主経路)"
            BedrockLLM["Bedrock LLM<br/>(Claude 3／Titan)"]
            BedrockVision["Bedrock Vision<br/>(Claude 3 Image or Rekognition+Titan)"]
            BedrockEmbed["Bedrock Titan Embeddings v2"]
        end

        %% ── AI 推論レイヤ ②：GPU コンテナ (OSS – Stretch)
        subgraph "GPU コンテナ群 (OSS Stretch)"
            direction TB
            GPU_EP["GPU Services Endpoint<br/>(ALB / VPC Link)"]
            GPU_EP --> FastAPI_GPU["FastAPI on Fargate<br/>(FactCheck & Suggest)"]
            FastAPI_GPU -. "LLM推論 (OSS)" .-> LLMSvc["LLM Service<br/>Gemma-3 on vLLM"]
            FastAPI_GPU -. "画像解析 (OSS)" .-> VisionSvc["Vision Service<br/>LLaVA-NeXT"]
        end

        %% ── FastAPI ⇆ Bedrock (MVP 実線)
        APIGW -- "/factcheck, /suggest" --> BedrockLLM
        APIGW -- "/vision" --> BedrockVision

        %% ── PPTX 抽出フロー
        LambdaUpload -- "(1) PPTXアップロード" --> S3PPTX[("S3: PPTX 原本バケット")]
        LambdaUpload -- "(2) 抽出キュー" --> SQSExtract["SQS: PPTX 抽出キュー"]
        SQSExtract --> ExtractorViaBatch["AWS Batch (+Spot)<br/>LibreOffice 抽出"]
        ExtractorViaBatch -- "(3) スライド JSON/PNG" --> S3ProcessedData[("S3: 抽出データ")]

        %% ── 埋め込み (MVP=Bedrock、OSSは破線)
        S3ProcessedData -- "(3a) 埋め込みキュー" --> SQSEmbed["SQS: 埋め込みキュー"]
        SQSEmbed --> LambdaEmbed["AWS Lambda: Embedding"]
        LambdaEmbed -- "(4) Titan Embeddings (MVP)" --> BedrockEmbed
        LambdaEmbed -. "(OSS bge/gte Stretch)" .-> VectorEmbedOSS["OSS Embedding (bge/gte)"]

        BedrockEmbed -- "(5) 保存" --> VectorDB["OpenSearch Serverless<br/>(Vector Index)"]
        VectorEmbedOSS -. "(5s) 保存" .-> VectorDB

        %% ── RAG / 外部情報
        APIGW -- "(6) Vector 検索" --> VectorDB
        APIGW -- "(7) Web/学術 API" --> ExternalAPIs["外部API (SerpAPI, Bing, arXiv)"]

        %% ── フィードバック & Judge
        LambdaFeedback -- "(8) DynamoDB 保存" --> FeedbackDB[("DynamoDB: Feedback")]
        LambdaFeedback -- "(9) Judge キュー" --> SQSJudge["SQS: Judge キュー"]
        SQSJudge --> JudgeConsumer["Judge Lambda"]
        JudgeConsumer -- "評価 (MVP: Bedrock)" --> BedrockLLM
        JudgeConsumer -. "評価 (Stretch: OSS)" .-> LLMSvc

        %% ── VPC エンドポイント (主要なもののみ)
        LambdaUpload --> VPCE_S3[("VPCE: S3")]
        LambdaEmbed --> VPCE_OpenSearch[("VPCE: OpenSearch")]

    end

    %% ─── MLOps ────────────────────────────────
    subgraph "MLOps & 開発支援"
        MLflow["MLflow"]
        DevPC["開発者 PC (RTX 5080)"]
        GitHub["GitHub Actions"]
        DevPC -- "実験管理" --> MLflow
        GitHub -- "CI/CD" --> FastAPI_GPU
    end

    %% ─── スタイリング ─────────────────────────
    classDef user fill:#f9f,stroke:#333,stroke-width:2px;
    classDef frontend fill:#9cf,stroke:#333,stroke-width:2px;
    classDef backend_serverless fill:#6c9,stroke:#333,stroke-width:2px;
    classDef bedrock fill:#d6a6ff,stroke:#333,stroke-width:2px;
    classDef backend_container fill:#396,stroke:#333,stroke-width:2px,color:white;
    classDef ai_model_container fill:#c9f,stroke:#333,stroke-width:2px;
    classDef storage fill:#fc9,stroke:#333,stroke-width:2px;
    classDef queue fill:#f69,stroke:#333,stroke-width:2px;
    classDef external fill:#ccc,stroke:#333,stroke-width:2px;
    classDef mlops fill:#fcc,stroke:#333,stroke-width:2px;

    class User user;
    class FE frontend;
    class APIGW,LambdaUpload,LambdaFeedback,LambdaEmbed backend_serverless;
    class BedrockLLM,BedrockVision,BedrockEmbed bedrock;
    class GPU_EP,FastAPI_GPU backend_container;
    class LLMSvc,VisionSvc ai_model_container;
    class S3PPTX,S3ProcessedData,VectorDB,FeedbackDB storage;
    class ExtractorViaBatch,JudgeConsumer queue;
    class SQSExtract,SQSEmbed,SQSJudge queue;
    class ExternalAPIs external;
    class MLflow,DevPC,GitHub mlops;
