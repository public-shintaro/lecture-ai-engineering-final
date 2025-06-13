# ----------------------------------------
# ベースイメージ
# ----------------------------------------
FROM python:3.11-slim

# 1) 必要パッケージのインストール
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libmagic1 \
        libreoffice-core \
        libreoffice-impress \
        unzip \
        curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws

# 2) 作業ディレクトリ
WORKDIR /app

# 3) 依存パッケージをコピーしてインストール
COPY backend/extraction_service/requirements.txt .
COPY .env .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 4) アプリケーションコードとテンプレートをコピー
#    appディレクトリの「中身」を作業ディレクトリ(/app)にコピー
COPY backend/extraction_service/app/ ./
#    ▼▼▼【修正点】templatesディレクトリのCOPY命令を正しく追加 ▼▼▼
#    templatesディレクトリの中身を作業ディレクトリ(/app)の中にtemplates/としてコピー
COPY backend/extraction_service/templates/ ./templates/

# 5) ポート設定
EXPOSE 8000

# 6) コンテナ起動時コマンド
#    WORKDIRが/appなので、main.pyを直接指定する
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
