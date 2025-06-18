#!/bin/bash

# スクリプトが失敗した場合に即座に終了する設定
set -e

# LocalStackのエンドポイントURL
ENDPOINT_URL=${AWS_ENDPOINT_URL:-http://localhost:4566}

echo "Waiting for LocalStack to be ready..."
# LocalStackが起動するまで最大30秒待機
until aws s3 ls --endpoint-url=$ENDPOINT_URL > /dev/null 2>&1; do
  >&2 echo "Localstack is unavailable - sleeping"
  sleep 1
done

echo "LocalStack is up - executing command"
echo "Initializing LocalStack resources..."

# S3バケットの作成
echo "Creating S3 bucket: ${UPLOAD_BUCKET}"
aws s3 mb s3://${UPLOAD_BUCKET} --endpoint-url=$ENDPOINT_URL || echo "S3 bucket ${UPLOAD_BUCKET} already exists."

# SQSキューの作成
echo "Creating SQS queue: ${EXTRACT_QUEUE_NAME}"
aws sqs create-queue --queue-name ${EXTRACT_QUEUE_NAME} --endpoint-url=$ENDPOINT_URL

# DynamoDBテーブルの作成

# ① slide_chunks
echo "Creating DynamoDB table: slide_chunks"
awslocal dynamodb create-table \
  --table-name slide_chunks \
  --attribute-definitions \
      AttributeName=slide_id,AttributeType=S \
      AttributeName=chunk_id,AttributeType=S \
  --key-schema \
      AttributeName=slide_id,KeyType=HASH \
      AttributeName=chunk_id,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  || echo "Table slide_chunks already exists."

# ② factcheck_results
echo "Creating DynamoDB table: factcheck_results"
awslocal dynamodb create-table \
  --table-name factcheck_results \
  --attribute-definitions \
      AttributeName=slide_id,AttributeType=S \
      AttributeName=id,AttributeType=S \
  --key-schema \
      AttributeName=slide_id,KeyType=HASH \
      AttributeName=id,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  || echo "Table factcheck_results already exists."
# ③ lecture_vector_store
echo "Creating DynamoDB table: lecture-vector-store-dev"
aws dynamodb create-table \
    --table-name lecture-vector-store-dev \
    --attribute-definitions \
        AttributeName=slide_id,AttributeType=S \
        AttributeName=chunk_id,AttributeType=S \
    --key-schema \
        AttributeName=slide_id,KeyType=HASH \
        AttributeName=chunk_id,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --global-secondary-indexes \
        "[
            {
                \"IndexName\": \"SlideIdIndex\",
                \"KeySchema\": [{\"AttributeName\":\"slide_id\",\"KeyType\":\"HASH\"}],
                \"Projection\":{
                    \"ProjectionType\":\"ALL\"
                },
                \"ProvisionedThroughput\": {
                    \"ReadCapacityUnits\": 5,
                    \"WriteCapacityUnits\": 5
                }
            }
        ]" \
    --endpoint-url=$ENDPOINT_URL || echo "DynamoDB table lecture-vector-store-dev already exists."

echo "LocalStack resources initialized successfully."
