# backend/api/v1/factcheck.py
import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from backend.aws_clients import bedrock_runtime as brt_factory
from backend.aws_clients import ddb as ddb_factory
from backend.services.factcheck import run_factcheck

router = APIRouter(tags=["factcheck"])


class FactcheckReq(BaseModel):
    slide_id: str = Field(..., description="PPTX のスライド ID")
    pages: Optional[List[int]] = Field(
        None, description="ページ番号のリスト。省略時は全ページを対象"
    )


@router.post("/factcheck", status_code=status.HTTP_200_OK)
async def post_factcheck(
    req: FactcheckReq,
    ddb=Depends(ddb_factory),
    brt=Depends(brt_factory),
):
    try:
        return await run_factcheck(
            slide_id=req.slide_id,
            pages=req.pages,
            ddb=ddb,
            brt=brt,
        )
    except ValueError as e:
        logging.error(f"FactCheck error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
