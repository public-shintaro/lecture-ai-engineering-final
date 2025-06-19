from __future__ import annotations

import asyncio
import json
import uuid
from datetime import datetime, timezone

from backend.aws_clients import bedrock_runtime as brt_factory
from backend.aws_clients import ddb as ddb_factory

CHUNKS_TABLE = "slide_chunks"
RESULT_TABLE = "factcheck_results"
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


async def _invoke_bedrock(prompt: str, brt) -> dict:
    body = json.dumps({"prompt": prompt, "max_tokens": 512, "temperature": 0})
    resp = await asyncio.to_thread(
        brt.invoke_model,
        modelId=MODEL_ID,
        body=body,
        accept="application/json",
        contentType="application/json",
    )
    # Claude のレスポンスは bytes -> str -> dict
    return json.loads(resp["body"].read())


async def run_factcheck(
    slide_id: str,
    *,
    ddb=None,
    brt=None,
) -> dict:
    """スライドをファクトチェックし、結果を DDB に保存して返す"""
    ddb = ddb or ddb_factory()
    brt = brt or brt_factory()

    chunks_tbl = ddb.Table(CHUNKS_TABLE)
    rows = chunks_tbl.query(
        KeyConditionExpression="slide_id = :sid",
        ExpressionAttributeValues={":sid": slide_id},
    )["Items"]
    if not rows:
        raise ValueError(f"slide_id={slide_id} not found")

    issues = []
    for c in rows:
        prompt = (
            "You are a fact-checking assistant.\n"
            f'Text: """{c["text"]}"""\n'
            "Return JSON with keys: issue_type, explanation, confidence."
        )
        res = await _invoke_bedrock(prompt, brt)
        issues.append({"chunk_id": c["chunk_id"], **res})

    item = {
        "slide_id": slide_id,
        "id": uuid.uuid4().hex,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "issues": issues,
    }
    ddb.Table(RESULT_TABLE).put_item(Item=item)
    return item
