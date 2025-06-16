from api.v1.upload import router as upload_router
from dotenv import load_dotenv
from fastapi import FastAPI

# アプリケーション起動時に .env ファイルを読み込む
load_dotenv()

app = FastAPI(
    title="Lecture-Slide Helper API",
    version="0.1.0",
)

app.include_router(upload_router, prefix="/api")
