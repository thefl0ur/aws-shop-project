import csv
import io
import json
import logging

from decimal import Decimal
from uuid import uuid4

import boto3

from pydantic import BaseModel, Field

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client("s3")
sqs_client = boto3.client("sqs")


class ProductSchema(BaseModel):
    title: str
    description: str | None = None
    price: Decimal = Field(gt=Decimal("0.0"))
    count: int = Field(ge=0)
    id: str = Field(default_factory=lambda: uuid4().hex)


def handler(event, context):
    logger.info("Incoming event: %s", json.dumps(event))

    queue_url_response = sqs_client.get_queue_url(QueueName="catalogItemsQueue")
    queue_url = queue_url_response["QueueUrl"]

    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    response = s3_client.get_object(Bucket=bucket, Key=key)

    wrap = io.TextIOWrapper(response["Body"], encoding="utf-8")
    csv_reader = csv.reader(wrap)

    for row in csv_reader:
        product = ProductSchema(
            title=row[0],
            description=row[1],
            price=Decimal(row[2]),
            count=int(row[3]),
        )
        sqs_client.send_message(
            QueueUrl=queue_url, MessageBody=product.model_dump_json()
        )

    move_file(bucket, key)


def move_file(bucket, key):
    new_key = "parsed/" + key[len("uploaded/") :]

    s3_client.copy_object(
        Bucket=bucket, CopySource={"Bucket": bucket, "Key": key}, Key=new_key
    )
    s3_client.delete_object(Bucket=bucket, Key=key)
