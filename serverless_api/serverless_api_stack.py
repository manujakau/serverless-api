from aws_cdk import (
    core,
    aws_dynamodb,
    aws_lambda,
    aws_s3,
    aws_iam,
    aws_apigateway
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

        #import s3
        code_bucket = aws_s3.Bucket.from_bucket_attributes(
            self,
            "code_bucket",
            bucket_name="code-bucket-lambda-cdk"
        )

        # lambda
        lambdaFunction01 = aws_lambda.Function(
            self,
            "lambdaFunction01",
            function_name="lambdaFunction01",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="index.labmda_handler",
            code=aws_lambda.S3Code(
                bucket=code_bucket,
                key="index.zip"
            ),
            timeout=core.Duration.seconds(60),
            reserved_concurrent_executions=1
        )

        lambdaFunction01.role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonDynamoDBFullAccess"
            )
        )
        lambdaFunction01.role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "CloudWatchFullAccess"
            )
        )

        # add API-GW
        api_gateway = aws_apigateway.LambdaRestApi(
            self,
            "apigateway01",
            handler=lambdaFunction01,
            proxy=False
        )

        health = api_gateway.root.add_resource('health')
        health.add_method('GET')

        item = api_gateway.root.add_resource('item')
        item.add_method('GET')
        item.add_method('POST')
        item.add_method('PATCH')
        item.add_method('DELETE')

        items = api_gateway.root.add_resource('items')
        items.add_method('GET')

        # output
        apigw_output = core.CfnOutput(
            self,
            "apigwOutput",
            value=f"{api_gateway.url}",
            description="web url for apigw"
        )
