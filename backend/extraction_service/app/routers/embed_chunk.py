# backend/extraction_service/app/routers/embed_chunk.py
from __future__ import annotations

import logging

from app.dependencies import vector_store  # aioboto3.Table -> VectorStore wrapper
from app.models import Chunk  # Pydanticモデル
from app.services.embedding import generate_embedding  # Titan 埋め込み util
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Chunk Embedding"])


class EmbedPayload(BaseModel):
    text: str
    slide_id: str
    idx: int = Field(ge=0)
    page: int = Field(gt=0)  # 1 origin


@router.post(
    "/embed",
    summary="Embed a single chunk and upsert into DynamoDB",
    status_code=status.HTTP_200_OK,
)
async def embed_chunk(payload: EmbedPayload):
    """
    1. Titan で text → embedding を生成
    2. DynamoDB (slide_chunks) に upsert
    """
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="text is empty")

    if not vector_store:
        raise HTTPException(status_code=503, detail="Vector store is not connected.")

    # ---- 1. Titan 埋め込み ----
    try:
        vector = generate_embedding(payload.text)  # returns List[float]
    except Exception as e:
        logger.error(f"Bedrock Titan error: {e}", exc_info=True)
        raise HTTPException(status_code=502, detail="Titan embedding failed")

    # ---- 2. DynamoDB upsert via VectorStore ----
    chunk_id = f"{payload.slide_id}-chunk-{payload.idx:04d}"
    chunk = Chunk(
        slide_id=payload.slide_id,
        chunk_id=chunk_id,
        text=payload.text,
        metadata={"page": payload.page},
        embedding=vector,
    )

    try:
        vector_store.add_chunk(chunk)  # <- async call
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DynamoDB error: {e}")

    return {"pk": chunk_id, "vector_dim": len(vector)}
