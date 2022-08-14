from aws_cdk import (
    core,
    aws_dynamodb,
    aws_lambda,
    aws_iam
)
from constructs import Construct


class ServerlessApiStack(core.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # dynamodb
        dynamodbLambda = aws_dynamodb.Table(
            self,
            "dynamodbLambda",
            table_name="dynamodbLambda",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
            server_side_encryption=True
        )

        # lambda
        try:
            with open("serverless_api/functions/function01.py", mode="r") as file:
                function_body = file.read()
        except OSError:
            print('File can not read')

        lambdaFunction01 = aws_lambda.Function(
            self,
            "lambdaFunction01",
            function_name="lambdaFunction01",
            runtime=aws_lambda.Runtime.PYTHON_3_6,
            handler="index.labmda_handler",
            code=aws_lambda.InlineCode(
                function_body
            ),
            timeout=core.Duration.seconds(60),
            reserved_concurrent_executions=1
        )

        lambdaFunction01.role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonDynamoDBFullAccess",
                "CloudWatchFullAccess"
            )
        )