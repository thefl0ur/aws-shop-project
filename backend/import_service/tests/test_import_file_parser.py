from unittest.mock import patch

import botocore
import pytest


def _build_s3_event(bucket, key):
    return {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": bucket},
                    "object": {"key": key},
                }
            }
        ]
    }


@pytest.mark.parametrize(
    ("body", "filename"),
    [
        (b"title,price\ntest,10.00\n", "products.csv"),
        (b"id,name\n1,foo\n2,bar\n3,baz\n", "items.csv"),
        (b"", "empty.csv"),
    ],
)
def test_csv_content(import_file_parser_mod, mock_s3, body, filename):
    mod = import_file_parser_mod
    bucket = "test-bucket"
    mock_s3.create_bucket(Bucket=bucket)
    mock_s3.put_object(Bucket=bucket, Key=f"uploaded/{filename}", Body=body)

    with (
        patch.object(mod, "s3_client", mock_s3),
        patch.object(mod, "logger") as mock_logger,
    ):
        event = _build_s3_event(bucket, f"uploaded/{filename}")
        mod.handler(event, {})

    actual_body = mock_s3.get_object(Bucket=bucket, Key=f"parsed/{filename}")[
        "Body"
    ].read()
    assert actual_body == body

    with pytest.raises(botocore.exceptions.ClientError) as exc:
        mock_s3.get_object(Bucket=bucket, Key=f"uploaded/{filename}")
    assert exc.value.response["Error"]["Code"] == "NoSuchKey"

    mock_logger.info.assert_called()
