import json
import logging

from aws_lambda_powertools.event_handler.api_gateway import (
    APIGatewayRestResolver,
    CORSConfig,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_handler(router):
    app = APIGatewayRestResolver(
        enable_validation=True,
        cors=CORSConfig(allow_origin="*"),
    )

    app.include_router(router)

    def handler(event, context):
        logger.info("Incoming event: %s", json.dumps(event))

        try:
            return app.resolve(event, context)

        except Exception:
            logger.exception("Unhandled exception")

            return {
                "statusCode": 500,
                "body": json.dumps({"message": "Internal server error"}),
            }

    return handler