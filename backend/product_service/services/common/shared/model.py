from decimal import Decimal
from uuid import uuid4

from pydantic import BaseModel, Field


class ProductModel(BaseModel):
    id: str
    title: str
    description: str | None = None
    price: Decimal = Field(gt=Decimal("0.0"))


class StockModel(BaseModel):
    product_id: str
    count: int = Field(ge=0)


class ProductWithStock(ProductModel):
    count: int = Field(ge=0)


class ProductCreate(BaseModel):
    title: str
    description: str | None = None
    price: Decimal = Field(gt=Decimal("0.0"))
    count: int = Field(ge=0)
    id: str = Field(default_factory=lambda: uuid4().hex)

    def to_product(self) -> ProductModel:
        return ProductModel(
            id=self.id,
            title=self.title,
            description=self.description,
            price=self.price,
        )

    def to_stock(self) -> StockModel:
        return StockModel(
            product_id=self.id,
            count=self.count,
        )
