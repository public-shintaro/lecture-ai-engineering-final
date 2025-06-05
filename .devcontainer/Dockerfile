# devcontainers の Python イメージをベース
FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# LibreOffice (headless) をインストール
RUN apt-get update && DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
        libreoffice-core libreoffice-impress libreoffice-writer \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
