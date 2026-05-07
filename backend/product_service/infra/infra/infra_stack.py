from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from constructs import Construct

class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        get_products_list = PythonFunction(
            self,
            "getProductsList",
            function_name="getProductsList",
            entry="../src",
            runtime=_lambda.Runtime.PYTHON_3_12,
            index="get_list/main.py",
            handler="handler",
        )

        get_products_by_id = PythonFunction(
            self,
            "getProductsById",
            function_name="getProductsById", 
            entry="../src",
            runtime=_lambda.Runtime.PYTHON_3_12,
            index="get_by_id/main.py",
            handler="handler",
        )

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

        product_by_id = products_resource.add_resource("{productId}")
        product_by_id.add_method(
            "GET", apigw.LambdaIntegration(get_products_by_id)
        )
