FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# システムパッケージの更新と、基本ツール・LibreOffice・Docker・GitHub CLIのインストール
# docker-composeはapt-getから削除
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
        libreoffice-core libreoffice-impress libreoffice-writer \
        docker.io \
        curl gpg \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" > /etc/apt/sources.list.d/github-cli.list \
    && apt-get update \
    && apt-get install -y gh

# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws

# --- ここから Docker Compose V2 のインストール部分 ---
# 最新版のDocker Composeを直接ダウンロードしてインストール
RUN DOCKER_COMPOSE_VERSION=v2.27.0 \
    && curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose \
    # docker compose (スペース区切り) コマンドを使えるようにプラグインとしても設定
    && mkdir -p /usr/local/lib/docker/cli-plugins \
    && ln -s /usr/local/bin/docker-compose /usr/local/lib/docker/cli-plugins/docker-compose
# --- ここまで ---

# uv (Pythonパッケージマネージャー) のインストール
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# uv を使って開発ツールをインストール
RUN /root/.local/bin/uv pip install --system ruff mypy

# コンテナ内でgitの所有権エラーが出ないようにするための設定
RUN git config --global --add safe.directory /workspaces/lecture-ai-engineering-final
