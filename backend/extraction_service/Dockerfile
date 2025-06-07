# ----------------------------------------
# ベースイメージ
# ----------------------------------------
FROM python:3.11-slim

# 1) 必要パッケージのインストール
#    * libmagic はファイルタイプ判定（exparso 内部）で稀に必要
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libmagic1 \
        curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 2) 作業ディレクトリ
WORKDIR /app

# 3) 依存パッケージをコピーしてインストール
COPY requirements.txt .
RUN cat requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 4) アプリケーションコードをコピー
COPY app ./app

# 5) ポート設定（FastAPI 既定 8080 として例示）
EXPOSE 8080

# 6) コンテナ起動時コマンド
#    pipでインストールされたコマンドのフルパスを直接指定して、PATH問題を回避
CMD ["/usr/local/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
