from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from backend.aws_clients import bedrock_runtime as brt_factory
from backend.aws_clients import ddb as ddb_factory
from backend.services.factcheck import run_factcheck

router = APIRouter(tags=["factcheck"])


class FactcheckReq(BaseModel):
    slide_id: str


@router.post(
    "/factcheck",
    status_code=status.HTTP_201_CREATED,
)
async def post_factcheck(
    req: FactcheckReq,
    ddb=Depends(ddb_factory),
    brt=Depends(brt_factory),
):
    try:
        return await run_factcheck(req.slide_id, ddb=ddb, brt=brt)
    except ValueError as e:
        raise HTTPException(404, str(e))
