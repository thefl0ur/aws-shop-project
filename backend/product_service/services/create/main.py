from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.exceptions import (
    BadRequestError,
    InternalServerError,
)
from pydantic import ValidationError
from shared.create_handler import create_handler
from shared.model import ProductCreate
from shared.service import get_product_service

router = Router()


@router.post("/products")
def create_product(product_data: dict):
    try:
        product = ProductCreate.model_validate(product_data)
    except ValidationError:
        raise BadRequestError("Invalid product data")

    try:
        product_service = get_product_service()
        product_service.create(product)
    except Exception:
        raise InternalServerError("Failed to save product")

    return product.model_dump()


handler = create_handler(router)
