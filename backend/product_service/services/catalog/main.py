import os
import json
import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.batch import (
    BatchProcessor,
    EventType,
    process_partial_response,
)
from aws_lambda_powertools.utilities.data_classes.sqs_event import SQSRecord

from shared.model import ProductCreate
from shared.service import get_product_service

logger = Logger()

processor = BatchProcessor(event_type=EventType.SQS)
sns_client = boto3.client("sns")


def product_handler(record: SQSRecord):
    product_service = get_product_service()
    product_data = json.loads(record.body)
    sns_topic_arn = os.environ["SNS_TOPIC_ARN"]

    try:
        product = ProductCreate.model_validate(product_data)
        product_service.create(product)
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="New Product Created!",
            Message=json.dumps(record.body),
            MessageAttributes={
                "count": {"DataType": "Number", "StringValue": str(product.count)}
            },
        )

    except Exception:
        logger.error("Exception")
        raise

    logger.info("Product created")


@logger.inject_lambda_context
def handler(event, context):
    return process_partial_response(
        event=event,
        record_handler=product_handler,
        processor=processor,
        context=context,
    )
