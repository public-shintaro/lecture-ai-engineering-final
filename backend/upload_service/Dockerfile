# backend/upload_service/Dockerfile

FROM python:3.11-slim

# アプリケーションの作業ディレクトリを設定
WORKDIR /app

# 依存パッケージの要件ファイルを先にコピーして、キャッシュを活用
COPY ./backend/api/v1/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# backendディレクトリの全てを/appにコピー
COPY ./backend .

# PYTHONPATHに/appを追加し、どこからでもモジュールを見つけられるようにする
ENV PYTHONPATH "${PYTHONPATH}:/app"