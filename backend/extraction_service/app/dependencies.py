import logging
import os

from dotenv import load_dotenv

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

from services.vector_store import VectorStore  # noqa: E402

logger = logging.getLogger(__name__)


# グローバルなサービス（DB接続など）の初期化をこのファイルに集約
vector_store = None
try:
    # VectorStoreの初期化を試みる
    vector_store = VectorStore()
    logger.info("VectorStore initialized successfully from dependencies.")
# ▼▼▼ あらゆる例外を捕捉できるように修正 ▼▼▼
except Exception as e:
    # どんなエラーが起きてもここで捕捉し、ログに詳細を記録する
    logger.critical(
        f"FATAL: Could not initialize VectorStore on startup. "
        f"The service will run without database functionality. Error: {e}",
        exc_info=True,  # 例外の詳細なトレースバックも記録する
    )
