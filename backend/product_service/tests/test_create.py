from decimal import Decimal

import pytest
from unittest.mock import patch

from aws_lambda_powertools.event_handler.exceptions import InternalServerError
from pydantic import ValidationError

from shared.model import ProductCreate


def test_create_product(product_service):
    product = ProductCreate(
        title="New Product",
        description="New Description",
        price=Decimal("25.00"),
        count=10,
    )
    product_service.create(product)

    retrieved = product_service.get_by_id(product.id)
    assert retrieved is not None
    assert retrieved.title == "New Product"
    assert retrieved.description == "New Description"
    assert retrieved.price == Decimal("25.00")
    assert retrieved.count == 10


@pytest.mark.parametrize("price", [Decimal("0"), Decimal("-10")])
def test_invalid_price(price):
    with pytest.raises(ValidationError):
        ProductCreate(
            title="Invalid Product",
            price=price,
            count=10,
        )


def test_invalid_count():
    with pytest.raises(ValidationError):
        ProductCreate(
            title="Invalid Count Product",
            price=Decimal("10.00"),
            count=-1,
        )


def test_without_description(product_service):
    product = ProductCreate(
        title="No Description",
        price=Decimal("15.00"),
        count=5,
    )
    product_service.create(product)

    retrieved = product_service.get_by_id(product.id)
    assert retrieved.description is None


def test_create_success(product_service):
    product = ProductCreate(
        title="Retrieve Test",
        description="Should be retrievable",
        price=Decimal("30.00"),
        count=20,
    )
    product_service.create(product)

    retrieved = product_service.get_by_id(product.id)
    assert retrieved is not None
    assert retrieved.title == "Retrieve Test"
    assert retrieved.count == 20


def test_internal_error(product_service):
    from create.routes import create_product

    with patch("create.routes.get_product_service", return_value=product_service):
        with patch.object(
            product_service, "create", side_effect=RuntimeError("DB error")
        ):
            with pytest.raises(InternalServerError):
                create_product(
                    {
                        "title": "Test",
                        "price": "10.00",
                        "count": 5,
                    }
                )
