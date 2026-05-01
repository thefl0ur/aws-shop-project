from aws_lambda_powertools.event_handler.api_gateway import APIGatewayRestResolver, CORSConfig

from get_list.routes import router

app = APIGatewayRestResolver(
    enable_validation=True,
    cors=CORSConfig(allow_origin="*"),
)
app.include_router(router)


def handler(event, context):
    return app.resolve(event, context)
