from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_s3 as s3,
)
from aws_cdk.aws_lambda_python_alpha import PythonFunction
from constructs import Construct


class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket.from_bucket_name(
            self, "ImportBucket",
            "my-products-bucket"   # plain name, same as what Lambda uses
        )
        
        import_products_file = PythonFunction(
            self,
            "importProductsFile",
            function_name="importProductsFile",
            entry="../src",
            runtime=_lambda.Runtime.PYTHON_3_12,
            index="import_products_file/main.py",
            handler="handler",
            environment={
                "BUCKET_NAME": bucket.bucket_name
            }
        )

        bucket.grant_put(import_products_file, "uploaded/*")

        api = apigw.RestApi(
            self,
            "ImportApi",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
            ),
        )

        import_products_resource = api.root.add_resource("import")
        import_products_resource.add_method(
            "GET",
            apigw.LambdaIntegration(import_products_file),
            request_parameters={
                "method.request.querystring.name": True
            }
        )
