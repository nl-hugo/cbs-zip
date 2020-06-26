import json
import logging
import os

import boto3
from botocore.exceptions import ClientError

import decimalencoder

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


def handler(event, context):
    zipcode = event['pathParameters']['zipcode']
    logging.info('Get zipcode f{zipcode}')

    try:
        response = table.get_item(
            Key={
                'version': '20190801',  # version
                'pc6': zipcode
            })
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
    else:
        result = f'No result for zipcode \'{zipcode}\''
        if 'Item' in response:
            result = response['Item']
        return {
            'statusCode': 200,
            'body': json.dumps(result, cls=decimalencoder.DecimalEncoder)
        }
