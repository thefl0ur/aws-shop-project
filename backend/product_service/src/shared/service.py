import os

from boto3.dynamodb.types import TypeSerializer

from shared.clients import dynamodb_client, dynamodb_resource
from shared.model import ProductWithStock, ProductCreate

class ProductService:
    def __init__(self, client, resource):
        self._resource = resource
        self._products_table = resource.Table(os.environ["PRODUCTS_TABLE"])
        self._stocks_table = resource.Table(os.environ["STOCKS_TABLE"])

        self._client = client
        self._serializer = TypeSerializer()

    def _serialize(self, item: dict) -> dict:
        return {k: self._serializer.serialize(v) for k, v in item.items()}

    def get_all(self) -> list[ProductWithStock]:
        products = self._products_table.scan()["Items"]
        stocks = {
            x["product_id"]: x for x in self._stocks_table.scan()["Items"]
        }
        return [
            ProductWithStock(
                **product, count=stocks.get(product["id"])["count"]
            )
            for product in products
            if product["id"] in stocks
        ]

    def get_by_id(self, product_id: str) -> ProductWithStock | None:
        product = self._products_table.get_item(Key={"id": product_id}).get("Item")
        stock = self._stocks_table.get_item(Key={"product_id": product_id}).get("Item")

        if not product:
            return None

        return ProductWithStock(**product, count=stock["count"])

    def create(self, product_data: ProductCreate) -> ProductWithStock:
        self._client.transact_write_items(
            TransactItems=[
                {
                    "Put": {
                        "TableName": self._products_table.name,
                        "Item": self._serialize(
                            product_data.to_product().model_dump()
                        ),
                        "ConditionExpression": "attribute_not_exists(product_id)",
                    }
                },
                {
                    "Put": {
                        "TableName": self._stocks_table.name,
                        "Item": self._serialize(
                            product_data.to_stock().model_dump()
                        ),
                        "ConditionExpression": "attribute_not_exists(product_id)",
                    }
                },
            ]
        )


product_service = ProductService(dynamodb_client, dynamodb_resource)