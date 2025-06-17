from fastapi import APIRouter

router = APIRouter()


@router.get("/factcheck/placeholder", tags=["factcheck"])
async def stub():
    """動作確認用のダミー。後で削除"""
    return {"msg": "stub"}
