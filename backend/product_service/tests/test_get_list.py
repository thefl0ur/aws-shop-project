from decimal import Decimal

import pytest

from shared.model import ProductCreate


@pytest.fixture
def sample_products(product_service):
    products = [
        ProductCreate(
            title="Product 1",
            description="Description 1",
            price=Decimal("10.00"),
            count=100,
        ),
        ProductCreate(
            title="Product 2",
            description="Description 2",
            price=Decimal("20.50"),
            count=50,
        ),
    ]
    for p in products:
        product_service.create(p)


def test_get_empty_list(product_service):
    result = product_service.get_all()
    assert result == []


def test_get_all(product_service, sample_products):
    result = product_service.get_all()
    assert len(result) == 2

