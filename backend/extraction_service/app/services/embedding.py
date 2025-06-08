import json
import logging
import os
from typing import List

import boto3
from fastapi import HTTPException

logger = logging.getLogger(__name__)

try:
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime", region_name=aws_region
    )
except Exception as e:
    logger.error(f"Failed to initialize Bedrock client: {e}")
    bedrock_runtime = None


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of texts using Amazon Titan Embeddings G1 - Text v2.
    """
    if not bedrock_runtime:
        raise ConnectionError("Bedrock client is not initialized.")

    embeddings: List[List[float]] = []
    for text in texts:
        if not text:
            embeddings.append([])
            continue

        body = json.dumps(
            {"inputText": text, "embeddingConfig": {"outputEmbeddingLength": 256}}
        )

        try:
            response = bedrock_runtime.invoke_model(
                body=body,
                modelId="amazon.titan-embed-text-v2:0",
                accept="application/json",
                contentType="application/json",
            )
            response_body = json.loads(response.get("body").read())
            embeddings.append(response_body.get("embedding"))
        except Exception as e:
            logger.error(f"Failed to get embedding from Bedrock: {e}")
            raise HTTPException(
                status_code=500, detail=f"Bedrock invoke_model failed: {e}"
            )

    return embeddings


# Contains AI-generated edits.
