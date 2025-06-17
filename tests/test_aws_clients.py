# tests/test_aws_clients.py
from backend import aws_clients


def test_ddb_s3_client_creation(monkeypatch):
    # LocalStack 用にエンドポイントを stub
    monkeypatch.setenv("AWS_ENDPOINT_URL", "http://localhost:4566")
    ddb = aws_clients.ddb()
    s3 = aws_clients.s3()

    # boto3 の型かどうか軽く見る
    assert ddb.meta.service_name == "dynamodb"
    assert s3.meta.service_model.service_name == "s3"
