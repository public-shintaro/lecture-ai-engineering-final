"""
共通 boto3 クライアント工場。
- LocalStack では AWS_ENDPOINT_URL, AWS_ACCESS_KEY_ID 等を .env で上書き
- 本番では環境変数を unset すれば通常の AWS エンドポイントに自動接続
"""

import os
from functools import lru_cache

import boto3
from botocore.config import Config

# デフォルト値
_DEFAULT_REGION = os.getenv("AWS_REGION", "us-east-1")  # デフォルトは us-east-1
_LOCAL_ENDPOINT = os.getenv("AWS_ENDPOINT_URL") or None


def _session():
    """
    boto3 Session を作成。profile 名は AWS_PROFILE で上書き可能。
    LocalStack の場合でも、session は同一で問題ない。
    """
    return boto3.Session(
        region_name=_DEFAULT_REGION,
        profile_name=os.getenv("AWS_PROFILE") or None,
    )


def _client(service: str, *, region=None, endpoint=None):
    """
    汎用クライアント生成関数。UnitTest で一度に差し替えたい場合は
    monkeypatch で aws_clients._client を patch するだけで済む。
    """
    return _session().client(
        service,
        region_name=region or _DEFAULT_REGION,
        endpoint_url=endpoint or _LOCAL_ENDPOINT,
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


def _resource(service: str, *, region=None, endpoint=None):
    return _session().resource(
        service,
        region_name=region or _DEFAULT_REGION,
        endpoint_url=endpoint or _LOCAL_ENDPOINT,
        config=Config(retries={"max_attempts": 3, "mode": "standard"}),
    )


# ------------------------------------------------------------
# エクスポート関数（FastAPI の Depends でそのまま使える）
# ------------------------------------------------------------


@lru_cache
def ddb():
    """DynamoDB resource (lazy singleton)"""
    return _resource("dynamodb")


@lru_cache
def s3():
    """S3 client (lazy singleton)"""
    return _client("s3")


@lru_cache
def bedrock_runtime():
    """
    Bedrock Runtime client
    ※ 現状 us-east-1 固定。`AWS_REGION` を上書きしないよう注意
    """
    return _client("bedrock-runtime", region="us-east-1", endpoint=None)
