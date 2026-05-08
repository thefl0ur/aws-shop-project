from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.event_handler.exceptions import InternalServerError

from shared.service import get_product_service

router = Router()


@router.get("/products")
def get_products():
    try:
        product_service = get_product_service()
        return [x.model_dump() for x in product_service.get_all()]
    except Exception as e:
        raise InternalServerError(str(e))
