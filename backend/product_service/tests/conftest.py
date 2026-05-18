import os
import sys
from pathlib import Path

import pytest

os.environ["PRODUCTS_TABLE"] = "Product"
os.environ["STOCKS_TABLE"] = "Stock"
os.environ["DYNAMODB_ENDPOINT"] = "http://localhost:8000"

SERVICES_DIR = Path(__file__).parent.parent / "services"
COMMON_PATH = str(SERVICES_DIR / "common")

if COMMON_PATH not in sys.path:
    sys.path.insert(0, COMMON_PATH)


@pytest.fixture
def mock_dynamodb():
    from moto import mock_aws

    with mock_aws():
        import boto3

        client = boto3.client("dynamodb", region_name="us-east-1")
        resource = boto3.resource("dynamodb", region_name="us-east-1")

        resource.create_table(
            TableName="Product",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        resource.create_table(
            TableName="Stock",
            KeySchema=[{"AttributeName": "product_id", "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": "product_id", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        yield {"client": client, "resource": resource}


@pytest.fixture
def product_service(mock_dynamodb):
    from shared.service import ProductService

    return ProductService(mock_dynamodb["client"], mock_dynamodb["resource"])
