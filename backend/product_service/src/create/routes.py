from aws_lambda_powertools.event_handler.exceptions import (
    InternalServerError,
    BadRequestError,
)
from aws_lambda_powertools.event_handler.api_gateway import Router

from pydantic import ValidationError

from shared.service import product_service
from shared.model import ProductCreate

router = Router()


@router.post("/products")
def get_product(product_data: dict):
    try:
        product = ProductCreate.model_validate(product_data)
    except ValidationError:
        raise BadRequestError("Invalid product data")

    try:
        product_service.create(product)
    except Exception:
        raise InternalServerError("Failed to save product")

    return product.model_dump()
