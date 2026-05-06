import sys

from decimal import Decimal
from uuid import uuid4
from pathlib import Path

import boto3

from faker import Faker
from faker_ecommerce import EcommerceProvider
from pydantic_settings import BaseSettings, SettingsConfigDict


# dirty hack
sys.path.append(
    str(Path(__file__).resolve().parent.parent / "backend/product_service/src")
)

from shared.model import ProductModel, StockModel


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        case_insensitive=True,
    )

    aws_access_key_id: str
    aws_secret_access_key: str
    region: str = "eu-central-1"


settings = Settings(_env_file="../.env")

fake = Faker()
fake.add_provider(EcommerceProvider)

session = boto3.Session()
dynamodb = session.resource(
    "dynamodb",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.region,
)

products_table = dynamodb.Table("Product")
stocks_table = dynamodb.Table("Stock")

ids = [uuid4().hex for _ in range(5)]

products = [
    ProductModel(
        id=uuid,
        title=fake.product_name(),
        description=fake.product_description(),
        price=Decimal(fake.price()[1:]),  # remove $
    )
    for uuid in ids
]

stocks = [StockModel(product_id=uuid, count=fake.pyint(max_value=10)) for uuid in ids]

with products_table.batch_writer() as writer:
    for p in products:
        writer.put_item(Item=p.model_dump())

with stocks_table.batch_writer() as writer:
    for s in stocks:
        writer.put_item(Item=s.model_dump())
