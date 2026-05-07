from decimal import Decimal

from pydantic import BaseModel, Field


class ProductModel(BaseModel):
    id: str
    title: str = ""
    description: str = ""
    price: Decimal = Field(gt=Decimal("0.0"))
