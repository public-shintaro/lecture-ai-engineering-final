#!/bin/sh

# スクリプトが失敗した場合に即座に終了する設定
set -e

echo "Starting FastAPI server in background..."
# 修正点: main.pyへのパスを単純化
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload &

echo "Starting SQS consumer in foreground..."
# 修正点: consumer.pyへのパスを単純化
python app/consumer.py

# バックグラウンド・ジョブが 1 つでもあればシェルが終了しないように
wait -n
