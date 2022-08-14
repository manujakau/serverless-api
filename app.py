#!/usr/bin/env python3
from aws_cdk import core

from serverless_api.serverless_api_stack import ServerlessApiStack


app = core.App()
serverless_stack = ServerlessApiStack(app, "ServerlessApiStack")

app.synth()
