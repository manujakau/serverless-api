from ast import Return
import logging
from decimal import Decimal
import json
from urllib import response
import boto3

ddbTableName = 'dynamodbLambda'
ddb = boto3.resource('dynamodb')
table = ddb.Table(ddbTableName)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


#from serverless_api.functions.custom_json_encoder import customJsonEncoder
# for zip package
#from custom_json_encoder import customJsonEncoder

getMethod = 'GET'
postMethod = 'POST'
patchMethod = 'PATCH'
deleteMethod = 'DELETE'

healthPath = "/health"
itemPath = '/item'
itemsPath = '/items'


class customJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


def functionBuildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=customJsonEncoder)
    return response


def getItem(itemId):
    try:
        response = table.get_item(
            key={
                'itemId': itemId
            }
        )
        if 'Item' in response:
            return functionBuildResponse(200, response['Item'])
        else:
            return functionBuildResponse(404, {'Message': 'ItemID: %s not found' % itemId})
    except:
        logger.exception('error getItem')


def getItems():
    try:
        response = table.scan()
        result = response['Item']
        while 'LastEvaluvatedKey' in response:
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluvatedKey'])
            result.extend(response['Item'])
        body = {
            'products': result
        }
        return functionBuildResponse(200, body)
    except:
        logger.exception('error getItems')


def putItem(requestBody):
    try:
        table.put_item(Item=requestBody)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': requestBody
        }
        return functionBuildResponse(200, body)
    except:
        logger.exception('error putItem')


def updateItem(itemId, updateKey, updateValue):
    try:
        response = table.update_item(
            Key={
                'itemId': itemId
            },
            UpdateExpression='set %s = :value' % updateKey,
            ExpressionAttributeValues={
                ':value': updateValue
            },
            ReturnValues='UPDATED_NEW'
        )
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'UpdateAttributes': response
        }
        return functionBuildResponse(200, body)
    except:
        logger.exception('error updateItem')


def deleteItem(itemId):
    try:
        response = table.delete_item(
            Key={
                'itemId': itemId
            },
            ReturnValues='ALL_OLD'
        )
        body = {
            'Operation': 'DELETE',
            'Message': 'SUCCESS',
            'deletedItem': response
        }
        return functionBuildResponse(200, body)
    except:
        logger.exception('error deleteItem')



def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']

    if httpMethod == getMethod and path == healthPath:
        response = functionBuildResponse(200)
    elif httpMethod == getMethod and path == itemPath:
        response = getItem(event['queryStringParameters']['itemId'])
    elif httpMethod == getMethod and path == itemsPath:
        response = getItems()
    elif httpMethod == postMethod and path == itemPath:
        response = putItem(json.loads(event['body']))
    elif httpMethod == patchMethod and path == itemPath:
        payLoad = json.loads(event['body'])
        response = updateItem(payLoad['itemId'],
                              payLoad['updateKey'], payLoad['updateValue'])
    elif httpMethod == deleteMethod and path == itemPath:
        payLoad = json.loads(event['body'])
        response = deleteItem(payLoad['itemId'])
    else:
        response = functionBuildResponse(404, 'Not Found')
    return response