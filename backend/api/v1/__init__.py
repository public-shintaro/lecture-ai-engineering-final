"""
backend/api/v1/__init__.py
v1 エンドポイントを一括管理する APIRouter を提供する
"""
from fastapi import APIRouter

# 個別ルーターを import（まだ存在しないファイルは後で作る）
from . import upload  # 既存
from . import factcheck  # ★ 今後作成

api_v1_router = APIRouter(prefix="/api/v1")

# include 順は自由。既存ルートが増えてもここに追加するだけ
api_v1_router.include_router(upload.router)
api_v1_router.include_router(factcheck.router)
