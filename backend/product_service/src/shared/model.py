from decimal import Decimal

from pydantic import BaseModel, Field


class ProductModel(BaseModel):
    id: str
    title: str
    description: str | None = None
    price: Decimal = Field(gt=Decimal("0.0"))


class StockModel(BaseModel):
    product_id: str
    count: int = Field(ge=0)