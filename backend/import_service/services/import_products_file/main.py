import os

import boto3

from aws_lambda_powertools.event_handler import Response
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.exceptions import (
    InternalServerError,
    BadRequestError,
)


from shared.create_handler import create_handler


router = Router()

s3_client = boto3.client("s3")


def generate_presigned_url(s3, bucket_name: str, file_name: str) -> str:
    try:
        return s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": bucket_name,
                "Key": f"uploaded/{file_name}",
                "ContentType": "text/csv",
            },
            ExpiresIn=3600,
        )
    except Exception:
        raise InternalServerError("Failed to prepare signed url")


@router.get("/import")
def import_products_file():
    file_name = router.current_event.get_query_string_value("name")
    if not file_name:
        raise BadRequestError("Missing 'name' query parameter")

    signed_url = generate_presigned_url(s3_client, os.environ["BUCKET_NAME"], file_name)

    return Response(status_code=200, content_type="text/plain", body=signed_url)


handler = create_handler(router)
