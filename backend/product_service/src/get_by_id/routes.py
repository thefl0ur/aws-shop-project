from aws_lambda_powertools.event_handler.exceptions import (
    InternalServerError,
    NotFoundError,
)
from aws_lambda_powertools.event_handler.api_gateway import Router

from shared.service import product_service


router = Router()


@router.get("/products/<product_id>")
def get_product(product_id: str):
    try:
        product = product_service.get_by_id(product_id)
    except Exception:
        raise InternalServerError("Failed to get data")

    if not product:
        raise NotFoundError(f"Product '{product_id}' not found")

    return product.model_dump()
