import csv
import io
import json
import logging

import boto3


logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client("s3")


def handler(event, context):
    logger.info("Incoming event: %s", json.dumps(event))

    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    response = s3_client.get_object(Bucket=bucket, Key=key)

    wrap = io.TextIOWrapper(response["Body"], encoding="utf-8")
    csv_reader = csv.reader(wrap)

    for row in csv_reader:
        logger.info(row)

    move_file(bucket, key)


def move_file(bucket, key):
    new_key = "parsed/" + key[len("uploaded/") :]

    s3_client.copy_object(
        Bucket=bucket, CopySource={"Bucket": bucket, "Key": key}, Key=new_key
    )
    s3_client.delete_object(Bucket=bucket, Key=key)
