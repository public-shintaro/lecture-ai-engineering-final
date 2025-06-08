import json
import logging
import os
from typing import List

import boto3

logger = logging.getLogger(__name__)

br = boto3.client(
    "bedrock-runtime",
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "amazon.titan-embed-text-v2:0")


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """Titan Embeddings v2 公式フォーマットに従い 1 文ずつ呼び出す"""
    vectors = []
    for t in texts:
        body = json.dumps({"inputText": t})
        resp = br.invoke_model(
            modelId=MODEL_ID,
            body=body,
            accept="application/json",
            contentType="application/json",
        )
        vectors.append(json.loads(resp["body"].read())["embedding"])
    return vectors


# Contains AI-generated edits.
