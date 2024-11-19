import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tenants')

def lambda_handler(event, context):
    try:
        response = table.scan()
        items = response.get('Items')

        return {
            'statusCode': 200,
            'body': json.dumps(items)
        }
    except (BotoCoreError, ClientError) as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error retrieving tenants: {str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'An unexpected error occurred: {str(e)}')
        }