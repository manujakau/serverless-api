import boto3, json

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

from serverless_api.functions.custom_json_encoder import customJsonEncoder

# for zip package
#from custom_json_encoder import customJsonEncoder

methodGet = 'GET'
methodPost = 'POST'
methodPatch = 'PATCH'
methodDelete = 'DELETE'

pathHealth = "/health"
pathItem = '/item'
pathItems = '/items'

