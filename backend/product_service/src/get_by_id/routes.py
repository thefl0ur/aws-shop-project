from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from aws_lambda_powertools.event_handler.api_gateway import Router

from shared.data import PRODUCTS

router = Router()


@router.get("/products/<product_id>")
def get_product(product_id: str):
    product = PRODUCTS.get(product_id)

    if not product:
        raise NotFoundError(f"Product '{product_id}' not found")
    return product.model_dump()
