import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI

# 全てのインポート処理が始まる前に、.envファイルの内容を環境変数に読み込む
load_dotenv()
print("--- DEBUGGING ENVIRONMENT VARIABLES ---")
access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
session_token = os.getenv("AWS_SESSION_TOKEN")
print(f"AWS_ACCESS_KEY_ID: {'[SET]' if access_key else '[NOT SET]'}")
# シークレットキーそのものは表示せず、存在有無だけ確認
print(f"AWS_SECRET_ACCESS_KEY: {'[SET]' if secret_key else '[NOT SET]'}")
# セッショントークンは空文字かどうかが重要なのでクォートで囲って表示
print(f"AWS_SESSION_TOKEN: {'[SET]' if session_token else '[NOT SET]'}'")
print("--- END DEBUGGING ---")
# --- ↑↑↑ ここまで追加 ↑↑↑ ---

# 各機能のルーターをインポート
from routers import document, factcheck, vision  # noqa: E402

# --- アプリケーション全体のロガー設定 ---
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --- FastAPIアプリケーションのセットアップ ---
app = FastAPI(
    title="AI-Powered Slide Analysis Service",
    description="An API service to extract, analyze, and fact-check presentation slides.",
    version="1.0.0",
)

# --- 各ルーターをアプリケーションに登録 ---
app.include_router(document.router)
app.include_router(factcheck.router)
app.include_router(vision.router)


@app.get("/health", summary="Health Check")
def health_check():
    """
    Simple health check endpoint to confirm the service is running.
    """
    logger.info("Health check endpoint was called.")
    return {"status": "ok"}


# Contains AI-generated edits.
