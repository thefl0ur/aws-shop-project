from shared.data import PRODUCTS
from get_list.routes import get_products


def test_get_list():
    data = get_products()
    assert data, "Expected results"
    assert len(data) == len(PRODUCTS)
