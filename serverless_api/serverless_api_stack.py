from aws_cdk import (
    core,
    aws_dynamodb
)
from constructs import Construct

class ServerlessApiStack(core.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        #dynamodb
        dynamodbLambda = aws_dynamodb.Table(
            self,
            "dynamodbLambda",
            partition_key=aws_dynamodb.Attribute(
                name="id",
                type=aws_dynamodb.AttributeType.STRING
            ),
            removal_policy=core.RemovalPolicy.DESTROY,
            server_side_encryption=True
        )