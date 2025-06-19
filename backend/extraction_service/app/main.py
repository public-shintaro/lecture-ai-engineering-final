import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .dependencies import get_vector_store

# 修正点: 相対パスでのインポートに変更
from .routers import document, factcheck, vision

# ロガーの設定
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # アプリケーション起動時に実行
    logging.info("Starting up...")
    # VectorStoreの初期化を確認
    try:
        get_vector_store()
        logging.info("VectorStore is available.")
    except Exception as e:
        logging.critical(f"Failed to get VectorStore on startup: {e}", exc_info=True)
    yield
    # アプリケーション終了時に実行
    logging.info("Shutting down...")


app = FastAPI(lifespan=lifespan)

# ルーターの登録
app.include_router(document.router)
app.include_router(factcheck.router)
app.include_router(vision.router)


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}
