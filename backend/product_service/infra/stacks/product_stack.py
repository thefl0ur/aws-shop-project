from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigw
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction, PythonLayerVersion
from constructs import Construct

class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        common = PythonLayerVersion(
            self,
            "SharedLayer",
            entry="services/common",
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_12],
            description="Shared utilities",
        )

        products_table = dynamodb.Table.from_table_name(self, "Product", "Product")
        stocks_table = dynamodb.Table.from_table_name(self, "Stock", "Stock")

        get_products_list = PythonFunction(
            self,
            "getProductsList",
            function_name="getProductsList",
            entry="services/get_list",
            runtime=_lambda.Runtime.PYTHON_3_12,
            index="main.py",
            handler="handler",
            environment={
                "PRODUCTS_TABLE": products_table.table_name,
                "STOCKS_TABLE": stocks_table.table_name,
                "DYNAMODB_ENDPOINT": "",
            },
            layers=[common],
        )

        get_products_by_id = PythonFunction(
            self,
            "getProductsById",
            function_name="getProductsById", 
            entry="services/get_by_id",
            runtime=_lambda.Runtime.PYTHON_3_12,
            index="main.py",
            handler="handler",
            environment={
                "PRODUCTS_TABLE": products_table.table_name,
                "STOCKS_TABLE": stocks_table.table_name,
                "DYNAMODB_ENDPOINT": "",
            },
            layers=[common],
        )

        create_product = PythonFunction(
            self,
            "createProduct",
            function_name="createProduct", 
            entry="services/create",
            runtime=_lambda.Runtime.PYTHON_3_12,
            index="main.py",
            handler="handler",
            environment={
                "PRODUCTS_TABLE": products_table.table_name,
                "STOCKS_TABLE": stocks_table.table_name,
                "DYNAMODB_ENDPOINT": "",
            },
            layers=[common],
        )

        products_table.grant_read_write_data(get_products_list)
        products_table.grant_read_write_data(get_products_by_id)
        products_table.grant_read_write_data(create_product)

        stocks_table.grant_read_write_data(get_products_list)
        stocks_table.grant_read_write_data(get_products_by_id)
        stocks_table.grant_read_write_data(create_product)

        api = apigw.RestApi(
            self,
            "ProductApi",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
            ),
        )

        products_resource = api.root.add_resource("products")
        products_resource.add_method(
            "GET", apigw.LambdaIntegration(get_products_list)
        )
        products_resource.add_method(
            "POST", apigw.LambdaIntegration(create_product)
        )

        product_by_id = products_resource.add_resource("{productId}")
        product_by_id.add_method(
            "GET", apigw.LambdaIntegration(get_products_by_id)
        )
