# tests/test_upload_service.py
import io
from unittest import mock

import pytest
from botocore.stub import Stubber

from backend.aws_clients import ddb as real_ddb
from backend.aws_clients import s3 as real_s3
from backend.services.upload import run_upload


@pytest.mark.asyncio
async def test_run_upload_with_stubbers():
    s3 = real_s3()
    ddb = real_ddb()

    with Stubber(s3) as s3_stub, Stubber(ddb.meta.client) as ddb_stub:
        s3_stub.add_response(
            "put_object",
            expected_params={
                "Bucket": "lecture-slide-files",
                "Key": mock.ANY,
                "Body": mock.ANY,
            },
            service_response={},
        )
        ddb_stub.add_response(
            "put_item",
            expected_params={"TableName": "slide_chunks", "Item": mock.ANY},
            service_response={},
        )

        dummy = io.BytesIO(b"bytes")
        dummy.filename = "demo.pptx"
        res = await run_upload(dummy, s3_client=s3, ddb_client=ddb)
        assert "slide_id" in res and res["slide_id"]
        assert res["s3_key"].endswith("demo.pptx")
