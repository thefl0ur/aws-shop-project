from decimal import Decimal

from aws_lambda_powertools.event_handler.exceptions import NotFoundError
import pytest
from unittest.mock import patch

from shared.model import ProductCreate


@pytest.fixture
def sample_product(product_service):
    product = ProductCreate(
        title="Test Product",
        description="Test Description",
        price=Decimal("15.00"),
        count=42,
    )
    product_service.create(product)
    return product


def test_get_by_id(product_service, sample_product):
    result = product_service.get_by_id(sample_product.id)
    assert result is not None
    assert result.id == sample_product.id
    assert result.title == sample_product.title
    assert result.count == sample_product.count


def test_service_not_found(product_service):
    result = product_service.get_by_id("nonexistent-id")
    assert result is None


def test_not_found_error(product_service):
    from get_by_id.routes import get_product

    with patch("get_by_id.routes.get_product_service", return_value=product_service):
        with pytest.raises(NotFoundError):
            get_product("nonexistent-id")
