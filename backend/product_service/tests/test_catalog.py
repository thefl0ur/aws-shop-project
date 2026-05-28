import json
from decimal import Decimal

import pytest
from unittest.mock import patch

from aws_lambda_powertools.utilities.data_classes.sqs_event import SQSRecord

from shared.model import ProductCreate


@pytest.fixture
def catalog_env(mock_dynamodb):
    import os
    import boto3

    sns = boto3.client("sns", region_name="us-east-1")
    sqs = boto3.client("sqs", region_name="us-east-1")

    topic = sns.create_topic(Name="catalog-test-topic")
    topic_arn = topic["TopicArn"]

    queue = sqs.create_queue(QueueName="catalog-test-queue")
    queue_url = queue["QueueUrl"]
    queue_arn = sqs.get_queue_attributes(
        QueueUrl=queue_url, AttributeNames=["QueueArn"]
    )["Attributes"]["QueueArn"]

    sns.subscribe(TopicArn=topic_arn, Protocol="sqs", Endpoint=queue_arn)

    with patch.dict(os.environ, {"SNS_TOPIC_ARN": topic_arn}):
        yield {"topic_arn": topic_arn, "queue_url": queue_url, "sqs": sqs}


def test_success(catalog_env, product_service):
    from catalog.main import product_handler

    product = ProductCreate(
        title="Test Product",
        description="Test Description",
        price=Decimal("25.00"),
        count=10,
    )

    record = SQSRecord({"body": json.dumps(product.model_dump(mode="json"))})

    with patch("catalog.main.get_product_service", return_value=product_service):
        product_handler(record)

    retrieved = product_service.get_by_id(product.id)
    assert retrieved is not None
    assert retrieved.title == "Test Product"
    assert retrieved.price == Decimal("25.00")
    assert retrieved.count == 10

    response = catalog_env["sqs"].receive_message(
        QueueUrl=catalog_env["queue_url"],
        WaitTimeSeconds=2,
    )
    messages = response.get("Messages", [])
    assert len(messages) == 1
    sns_envelope = json.loads(messages[0]["Body"])
    assert sns_envelope["Subject"] == "New Product Created!"
    count_attr = sns_envelope.get("MessageAttributes", {}).get("count", {})
    assert count_attr["Value"] == "10"


def test_service_error(catalog_env, product_service):
    from catalog.main import product_handler

    product = ProductCreate(
        title="Error Product",
        price=Decimal("10.00"),
        count=5,
    )

    record = SQSRecord({"body": json.dumps(product.model_dump(mode="json"))})

    with patch("catalog.main.get_product_service", return_value=product_service):
        with patch.object(
            product_service, "create", side_effect=RuntimeError("DB error")
        ):
            with pytest.raises(RuntimeError):
                product_handler(record)

    retrieved = product_service.get_by_id(product.id)
    assert retrieved is None

    response = catalog_env["sqs"].receive_message(
        QueueUrl=catalog_env["queue_url"],
        WaitTimeSeconds=1,
    )
    assert len(response.get("Messages", [])) == 0
