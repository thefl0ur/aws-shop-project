import os

import boto3

from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.exceptions import (
    InternalServerError,
    BadRequestError,
)


from shared.create_handler import create_handler


router = Router()

s3_client = boto3.client("s3")


@router.post("/import")
def create_product():
    file_name = router.current_event.get_query_string_value("name")
    if not file_name:
        raise BadRequestError("Missing 'name' query parameter")

    signed_url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": os.environ["BUCKET_NAME"],
            "Key": f"uploaded/{file_name}",
            "ContentType": "text/csv",
        },
        ExpiresIn=3600,
    )

    return signed_url


handler = create_handler(router)