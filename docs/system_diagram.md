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

        %% ── バックエンド処理API (FastAPI)
        APIGW -- "/factcheck, /suggest, /vision" --> FastAPI_Logic["FastAPI on Fargate <br/> (FactCheck, Suggest Logic & AI Orchestration)"]

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
            GPU_EP --> FastAPI_GPU["FastAPI on Fargate (OSS Proxy)<br/>(FactCheck & Suggest OSS Path)"]
            FastAPI_GPU -. "LLM推論 (OSS)" .-> LLMSvc["LLM Service<br/>Gemma-3 on vLLM"]
            FastAPI_GPU -. "画像解析 (OSS)" .-> VisionSvc["Vision Service<br/>LLaVA-NeXT"]
        end

        %% ── FastAPI ⇆ Bedrock (MVP 実線)
        FastAPI_Logic -- "LLM推論 (MVP: Bedrock)" --> BedrockLLM
        FastAPI_Logic -- "Vision処理 (MVP: Bedrock)" --> BedrockVision
        FastAPI_Logic -. "LLM/Vision (Stretch: OSS via GPU_EP)" .-> GPU_EP


        %% ── PPTX 抽出フロー
        LambdaUpload -- "(1) PPTXアップロード" --> S3PPTX[("S3: PPTX 原本バケット")]
        LambdaUpload -- "(2) 抽出キュー" --> SQSExtract["SQS: PPTX 抽出キュー"]
        SQSExtract --> ExtractorViaBatch["AWS Batch (+Spot)<br/>LibreOffice 抽出 (Exparso)"]
        ExtractorViaBatch -- "(3) スライド JSON/PNG" --> S3ProcessedData[("S3: 抽出データ")]

        %% ── 埋め込み (MVP=Bedrock、OSSは破線)
        S3ProcessedData -- "(3a) 埋め込みキュー" --> SQSEmbed["SQS: 埋め込みキュー"]
        SQSEmbed --> LambdaEmbed["AWS Lambda: Embedding"]
        LambdaEmbed -- "(4) Titan Embeddings (MVP)" --> BedrockEmbed
        LambdaEmbed -. "(OSS bge/gte Stretch)" .-> VectorEmbedOSS["OSS Embedding (bge/gte)"]

        BedrockEmbed -- "(5) 保存" --> VectorDB["OpenSearch Serverless<br/>(Vector Index)"]
        VectorEmbedOSS -. "(5s) 保存" .-> VectorDB

        %% ── RAG / 外部情報
        FastAPI_Logic -- "(6) Vector 検索 (RAG)" --> VectorDB
        FastAPI_Logic -- "(7) Web/学術 API (RAG)" --> ExternalAPIs["外部API (SerpAPI, Bing, arXiv)"]

        %% ── フィードバック & Judge
        LambdaFeedback -- "(8) DynamoDB 保存" --> FeedbackDB[("DynamoDB: Feedback")]
        LambdaFeedback -- "(9) Judge キュー" --> SQSJudge["SQS: Judge キュー"]
        SQSJudge --> JudgeConsumer["Judge Lambda"]
        JudgeConsumer -- "評価 (MVP: Bedrock)" --> BedrockLLM
        JudgeConsumer -. "評価 (Stretch: OSS)" .-> LLMSvc
        %% LLMSvcはGPUコンテナ群のOSS LLMを指す想定

        %% ── VPC エンドポイント (主要なもののみ)
        VPCE_S3[("VPC Endpoint <br/> S3")]
        VPCE_OpenSearch[("VPC Endpoint <br/> OpenSearch")]
        FastAPI_Logic --> VPCE_S3
        FastAPI_Logic --> VPCE_OpenSearch
    end

    %% ─── MLOps & 開発支援 ────────────────────────
    subgraph "MLOps & 開発支援"
        DevPC["開発者 PC (Dev Container)"]

        subgraph "ローカル開発スタック (docker-compose)"
            direction LR
            DevPC -- "docker compose up" --> ComposeServices{{"docker-compose.dev.yml"}}
            ComposeServices --> ExtractionSvc["Extraction Service"]
            ComposeServices --> MLflow["MLflow Tracking Server"]
        end

        DevPC -- "API Test" --> ExtractionSvc
        DevPC -- "実験管理" --> MLflow

        GitHub["GitHub Actions"] -- "CI/CD" --> FastAPI_Logic
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
    classDef service_compute fill:#eef,stroke:#346,stroke-width:1px;

    class User user;
    class FE frontend;
    class APIGW,LambdaUpload,LambdaFeedback,LambdaEmbed,JudgeConsumer backend_serverless;
    class BedrockLLM,BedrockVision,BedrockEmbed bedrock;
    class FastAPI_Logic,GPU_EP,FastAPI_GPU backend_container;
    class LLMSvc,VisionSvc ai_model_container;
    class S3PPTX,S3ProcessedData,VectorDB,FeedbackDB storage;
    class ExtractorViaBatch service_compute;
    class SQSExtract,SQSEmbed,SQSJudge queue;
    class ExternalAPIs external;
    class DevPC,GitHub mlops;
    class MLflow,ExtractionSvc,ComposeServices backend_container;
    class VectorEmbedOSS ai_model_container;
    class VPCE_S3,VPCE_OpenSearch storage;
