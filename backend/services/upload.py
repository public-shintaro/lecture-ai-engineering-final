# backend/services/upload.py
import os
from io import BytesIO
from typing import Dict, List

import httpx
from fastapi import UploadFile

RAW_BUCKET = os.getenv("UPLOAD_BUCKET", "lecture-slide-files")
CHUNK_BUCKET = os.getenv("CHUNK_BUCKET", "lecture-slide-chunks")

# Extraction Service のベース URL（docker-compose の service 名などに合わせる）
EXTRACT_HOST = os.getenv("EXTRACTION_API_URL", "http://extraction:8080")
EXTRACT_URL = f"{EXTRACT_HOST}/extract"
EMBED_URL = f"{EXTRACT_HOST}/embed"


async def run_upload_sync(
    file: UploadFile,
    slide_id: str,
    *,
    s3_client,
) -> Dict[str, str | int]:
    """
    1. PPTX を RAW_BUCKET に保存
    2. Extraction Service `/extract` へ同期 POST → [{idx, s3_key}, ...] 取得
    3. 各チャンク本文を S3 から取得し `/embed` へ同期 POST
    4. 結果としてチャンク数を返す
    """
    # 0. アップロードファイルをメモリに保持
    data: bytes = await file.read()  # ★ ここで読んで以後は閉じてもOK
    buffer = BytesIO(data)

    # ----------------------------------------
    # 1. 元 PPTX を S3 にアップロード
    # ----------------------------------------
    raw_key = f"uploads/{slide_id}.pptx"
    buffer.seek(0)

    s3_client.upload_fileobj(
        Fileobj=buffer,
        Bucket=RAW_BUCKET,
        Key=raw_key,
        ExtraArgs={"ContentType": file.content_type},  # ★ 追加
    )

    # ----------------------------------------
    # 2. Extraction Service へバイナリ POST
    #    返り値: [{"idx": 0, "s3_key": "slide/.../chunk_000.txt"}, ...]
    # ----------------------------------------
    buffer = BytesIO(data)  # ★ 再生成し直せば close 問題なし
    async with httpx.AsyncClient(timeout=180) as client:
        resp = await client.post(
            EXTRACT_URL,
            files={"file": (file.filename, buffer, file.content_type)},
            data={"slide_id": slide_id},
        )
    resp.raise_for_status()
    chunk_meta: List[dict] = resp.json()

    # ----------------------------------------
    # 3. 各チャンクの埋め込み生成を Extraction Service に依頼
    #    (Upload API はテキストを取り出して /embed に渡すだけ)
    # ----------------------------------------
    for meta in chunk_meta:
        obj = s3_client.get_object(Bucket=CHUNK_BUCKET, Key=meta["s3_key"])
        text = obj["Body"].read().decode("utf-8")

        async with httpx.AsyncClient(timeout=60) as client:
            embed_resp = await client.post(
                EMBED_URL,
                json={  # ★page を追加
                    "text": text,
                    "slide_id": slide_id,
                    "idx": meta["idx"],
                    "page": meta["page"],
                },
            )
        embed_resp.raise_for_status()  # 失敗時は例外を上げて FastAPI が 5xx 返す
    file.file.close()  # ★ FD 解放

    # ----------------------------------------
    # 4. 呼び出し元 (/upload) へレスポンス
    # ----------------------------------------
    return {
        "slide_id": slide_id,
        "s3_key": raw_key,
        "chunks": len(chunk_meta),
    }
