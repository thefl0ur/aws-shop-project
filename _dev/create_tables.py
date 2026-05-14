import boto3
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        case_insensitive=True,
    )

    aws_access_key_id: str
    aws_secret_access_key: str
    region: str = "eu-central-1"
    dynamodb_endpoint: str | None = None


settings = Settings(_env_file="../.env")

session = boto3.Session()
dynamodb = session.resource(
    "dynamodb",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.region,
    endpoint_url=settings.dynamodb_endpoint,
)

products_table = dynamodb.Table("Product")
stocks_table = dynamodb.Table("Stock")


def create_table(table_name, key):
    dynamodb.create_table(
        TableName=table_name,
        AttributeDefinitions=[
            {
                "AttributeName": key,
                "AttributeType": "S",
            },
        ],
        KeySchema=[
            {
                "AttributeName": key,
                "KeyType": "HASH",
            },
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 3,
            "WriteCapacityUnits": 3,
        },
    )


create_table("Product", "id")
create_table("Stock", "product_id")
