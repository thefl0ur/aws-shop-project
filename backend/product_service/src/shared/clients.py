import os
import boto3

dynamodb_resource = boto3.resource(
    "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT") or None
)
dynamodb_client = boto3.client(
    "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT") or None
)
