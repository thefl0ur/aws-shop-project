from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    CfnOutput,
)
from constructs import Construct


class AuthorizationServiceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        user = self.node.try_get_context("test_user")
        password = self.node.try_get_context("test_password")

        self.authorizer_lambda = _lambda.Function(
            self,
            "basicAuthorizer",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="main.handler",
            code=_lambda.Code.from_asset("services/basic_auth"),
            environment={user: password},
        )
        self.authorizer_lambda.add_permission(
            "AllowApiGatewayInvoke",
            principal=iam.ServicePrincipal("apigateway.amazonaws.com"),
        )
        CfnOutput(
            self,
            "BasicAuthorizerArnExport",
            value=self.authorizer_lambda.function_arn,
            export_name="BasicAuthorizerArn",
        )
