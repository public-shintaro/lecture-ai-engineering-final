# backend/services/factcheck.py
from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from json import JSONDecodeError
from typing import Any, Dict, List, Optional

from boto3.dynamodb.conditions import Key

from backend.aws_clients import bedrock_runtime as brt_factory
from backend.aws_clients import ddb as ddb_factory

# -----------------------------
CHUNK_TABLE = os.getenv("VECTOR_TABLE_NAME", "lecture-vector-store-dev")  # ★ 統一
RESULT_TABLE = "factcheck_results"
MODEL_ID = "us.amazon.nova-lite-v1:0"
TOP_K = 5
# -----------------------------
logging.basicConfig(level=logging.INFO)


def _safe_json_from_text(text: str) -> dict:
    # 1) コードブロックがあれば中身だけ抜く
    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", text, flags=re.I)
    cleaned = (m.group(1) if m else text).strip()

    # 2) 先頭の { または [
    start = re.search(r"[\{\[]", cleaned)
    if not start:
        raise ValueError("No JSON start char found in Bedrock response")

    snippet = cleaned[start.start() :]

    # 3) 一発パース or 末尾括弧までスライス
    try:
        obj = json.loads(snippet)
    except JSONDecodeError:
        end_brace = snippet.rfind("}")
        end_bracket = snippet.rfind("]")
        obj = json.loads(snippet[: max(end_brace, end_bracket) + 1])

    return {"issues": obj} if isinstance(obj, list) else obj


async def _invoke_bedrock(prompt: str, brt) -> dict:
    """
    Amazon Nova Lite v1 は Bedrock **Messages API** で呼び出す。
      * 入力 JSON:  {"schemaVersion":"messages-v1", "messages":[ ... ]}
      * system メッセージや user メッセージを array で渡す
      * レスポンス: {"output":{"message":{"content":[{"text":"…"}]}}}
    """
    body = json.dumps(
        {
            "schemaVersion": "messages-v1",
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}],
                }
            ],
        }
    )
    resp = await asyncio.to_thread(
        brt.invoke_model,
        modelId=MODEL_ID,
        body=body,
        accept="application/json",
        contentType="application/json",
    )
    payload = json.loads(resp["body"].read())
    try:
        output_text: str = payload["output"]["message"]["content"][0]["text"]
    except (KeyError, IndexError) as e:
        raise ValueError(f"Unexpected Bedrock response format: {payload}") from e

    # プロンプトで "Return JSON ..." と指示しているので、さらにパース
    # -------- robust JSON extraction --------
    try:
        return json.loads(output_text)  # ★一発で通ればそれで OK
    except JSONDecodeError:
        return _safe_json_from_text(output_text)  # ★フォールバック


def _build_per_page_prompt(page_num: int, page_text: str) -> str:
    return (
        "You are a meticulous fact-checking assistant.\n"
        f"Page: {page_num}\n"
        f'Text: """{page_text}"""\n'
        "For each factual statement, judge correctness.\n"
        "Return JSON list named `issues`, each item with:\n"
        "  • statement\n  • verdict (true/false/uncertain)\n"
        "  • explanation\n  • confidence (0-1)\n"
    )


def _build_summary_prompt(slide_id: str, per_page_results: list[dict]) -> str:
    return (
        f"Slide ID {slide_id} overall assessment.\n"
        "Input is JSON array of per-page results.\n"
        "Summarize major errors, common patterns, and overall reliability "
        "(score 0-1). Return JSON with keys:\n"
        "  • summary\n  • overall_score\n"
    )


async def _fetch_pages_for_slide(
    slide_id: str, ddb, requested_pages: Optional[List[int]]
) -> List[int]:
    """
    pages が None の場合、chunk_id 末尾4桁からページ番号を抽出して返す
    """
    if requested_pages:
        return requested_pages

    rows = ddb.Table(CHUNK_TABLE).query(  # ★ テーブル名
        KeyConditionExpression=Key("slide_id").eq(slide_id),  # ★ Key() を使用
        ProjectionExpression="chunk_id",
    )["Items"]

    pages = sorted({int(r["chunk_id"][-4:]) for r in rows})
    if not pages:
        raise ValueError(f"slide_id={slide_id} not found")
    return pages if requested_pages is None else requested_pages


def _to_dynamo(obj):
    """Recursively convert floats to Decimal so boto3 can serialize."""
    if isinstance(obj, float):
        return Decimal(str(obj))  # avoid binary-float issues
    if isinstance(obj, list):
        return [_to_dynamo(v) for v in obj]
    if isinstance(obj, dict):
        return {k: _to_dynamo(v) for k, v in obj.items()}
    return obj


async def run_factcheck(
    slide_id: str,
    pages: Optional[List[int]] = None,
    *,
    ddb=None,
    brt=None,
) -> Dict[str, Any]:
    ddb = ddb or ddb_factory()
    brt = brt or brt_factory()

    # 1. 対象ページ
    logging.info(f"FactCheck: slide_id={slide_id}, pages={pages}")
    target_pages = await _fetch_pages_for_slide(slide_id, ddb, pages)

    # 2. 並列でページ処理
    logging.info(
        f"FactCheck: processing {len(target_pages)} pages for slide_id={slide_id}"
    )

    async def _process_page(page_num: int) -> dict:
        prefix = f"{slide_id}-chunk-{page_num:04d}"
        rows = ddb.Table(CHUNK_TABLE).query(
            KeyConditionExpression=Key("slide_id").eq(slide_id)
            & Key("chunk_id").begins_with(prefix),
        )["Items"]

        if not rows:
            return {"page": page_num, "issues": [], "note": "no_chunks_found"}

        page_text = "\n".join(r["text"] for r in rows)
        res = await _invoke_bedrock(_build_per_page_prompt(page_num, page_text), brt)
        return {"page": page_num, **res}

    logging.info(f"FactCheck: invoking Bedrock for {len(target_pages)} pages")
    per_page_results = await asyncio.gather(*(_process_page(p) for p in target_pages))

    # 3. 要約
    logging.info(f"FactCheck: summarizing results for slide_id={slide_id}")
    slide_summary = None
    if len(per_page_results) > 1:
        slide_summary = await _invoke_bedrock(
            _build_summary_prompt(slide_id, per_page_results), brt
        )

    # 4. 保存
    print(f"FactCheck: saving results for slide_id={slide_id}")
    item = {
        "result_id": uuid.uuid4().hex,
        "slide_id": slide_id,
        "evaluated_pages": target_pages,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "per_page_results": per_page_results,
        "slide_summary": slide_summary,
    }
    ddb.Table(RESULT_TABLE).put_item(Item=_to_dynamo(item))

    # 5. レスポンス
    return {
        "per_page_results": per_page_results,
        **({"slide_summary": slide_summary} if slide_summary else {}),
    }
