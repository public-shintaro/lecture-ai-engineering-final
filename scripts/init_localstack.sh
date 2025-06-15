#!/usr/bin/env bash

# S3バケットを作成
awslocal s3 mb s3://slides-upload-dev

# SQSキューを作成
awslocal sqs create-queue --queue-name slide-extract-queue
