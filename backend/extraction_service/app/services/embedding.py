import json
import logging
import os

import boto3

logger = logging.getLogger(__name__)

# --- 定数とクライアントをモジュールレベルで初期化 ---
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "amazon.titan-embed-text-v2:0")

# boto3クライアントは一度だけ初期化して再利用するのが効率的
try:
    BEDROCK_RUNTIME = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "ap-northeast-1"),
    )
except Exception as e:
    logger.critical(f"Failed to initialize Bedrock client: {e}", exc_info=True)
    BEDROCK_RUNTIME = None


def generate_embedding(text: str) -> list[float] | None:
    """
    単一のテキストからベクトル埋め込みを生成する。
    """
    if not BEDROCK_RUNTIME:
        logger.error("Bedrock client is not available. Cannot generate embedding.")
        return None

    try:
        # BedrockのAPIに合わせてリクエストボディを作成
        body = json.dumps({"inputText": text})

        # モデルを呼び出し
        response = BEDROCK_RUNTIME.invoke_model(
            modelId=MODEL_ID,
            body=body,
            accept="application/json",
            contentType="application/json",
        )

        # レスポンスからベクトル部分を抽出して返す
        response_body = json.loads(response["body"].read())
        return response_body["embedding"]

    except Exception:
        logger.error(
            f"Failed to generate embedding for text: '{text[:50]}...'", exc_info=True
        )
        return None
