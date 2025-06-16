sequenceDiagram
    title: ファイルアップロードからDB格納までのシーケンス図

    participant User as あなた (or テスト)
    participant UploadService as upload_service
    participant S3
    participant SQS as 伝言板 (SQS)
    participant Consumer as consumer.py (職人)
    participant DynamoDB

    User->>+UploadService: 1. PPTXファイルとslide_idをアップロード
    UploadService->>S3: 2. ファイルをS3に保存
    UploadService->>SQS: 3. 処理依頼メッセージを送信
    UploadService-->>-User: 4. 受付完了 (HTTP 200 OK)

    Note over Consumer, SQS: (非同期処理)

    Consumer->>+SQS: 5. 新しい仕事がないか監視 (Polling)
    SQS-->>-Consumer: 6. 処理依頼メッセージを渡す

    Consumer->>S3: 7. メッセージを元にS3からPPTXをDL
    
    Note right of Consumer: 8. ファイルを解析・チャンク化・ベクトル化

    loop 各チャンクのループ
        Consumer->>DynamoDB: 9. チャンクデータをDBに保存
    end
    
    Consumer->>+SQS: 10. 完了した仕事のメッセージを削除
    SQS-->>-Consumer: 削除完了