from dotenv import load_dotenv
from fastapi import FastAPI

from backend.api.v1 import api_v1_router

# アプリケーション起動時に .env ファイルを読み込む
load_dotenv()

app = FastAPI(
    title="Lecture-Slide Helper API",
    version="0.1.0",
)

app.include_router(api_v1_router)
