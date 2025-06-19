# backend/extraction_service/Dockerfile (最終修正版)

FROM python:3.11-slim

# LibreOffice が無人インストール＆ headless で動くように
ENV DEBIAN_FRONTEND=noninteractive \
    HOME=/tmp               # soffice が $HOME を参照するため

# 1) 必要パッケージのインストール
# build-essential等は不要なので削除し、イメージを軽量化
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libreoffice-core \
        libreoffice-common \
        libreoffice-draw \
        libreoffice-impress \
        libmagic1 \
        unzip \
        curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 2) 作業ディレクトリ
WORKDIR /app

# 3) 依存パッケージをコピーしてインストール (パスを単純化)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) アプリケーションコードとその他ファイルをコピー (パスを単純化)
# appディレクトリ、templatesディレクトリ、start.shなどをWORKDIR(/app)にコピー
COPY ./app ./app
COPY ./templates ./templates
COPY ./start.sh .
