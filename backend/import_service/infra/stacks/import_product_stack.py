from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_s3 as s3,
    aws_s3_notifications as s3n,
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

        bucket = s3.Bucket.from_bucket_name(
            self,
            "ImportBucket",
            self.node.try_get_context("bucket_name"),
        )

        import_products_file = PythonFunction(
            self,
            "importProductsFile",
            function_name="importProductsFile",
            entry="services/import_products_file",
            runtime=_lambda.Runtime.PYTHON_3_12,
            index="main.py",
            handler="handler",
            environment={"BUCKET_NAME": bucket.bucket_name},
            layers=[common],
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
            request_parameters={"method.request.querystring.name": True},
        )

        import_file_parser = PythonFunction(
            self,
            "ParserHandler",
            function_name="importFileParser",
            entry="services/import_file_parser",
            runtime=_lambda.Runtime.PYTHON_3_12,
            index="main.py",
            handler="handler",
        )
        bucket.grant_read_write(import_file_parser)
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.LambdaDestination(import_file_parser),
            s3.NotificationKeyFilter(prefix="uploaded/"),
        )
