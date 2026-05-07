from aws_lambda_powertools.event_handler.api_gateway import Router

from shared.data import PRODUCTS

router = Router()


@router.get("/products")
def get_products():
    return [p.model_dump() for _, p in PRODUCTS.items()]
