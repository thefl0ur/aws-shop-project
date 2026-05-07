import random
from uuid import uuid4

from aws_lambda_powertools.event_handler.exceptions import NotFoundError
import pytest

from shared.data import PRODUCTS
from get_by_id.routes import get_product


def test_get_success():
    id, data = random.choice(list(PRODUCTS.items()))
    result = get_product(id)
    assert result, "Result expected"
    assert result["id"] == data.id


def test_get_not_found():
    with pytest.raises(NotFoundError):
        get_product(uuid4().hex)
