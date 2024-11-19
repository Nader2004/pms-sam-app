import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cleaning_service_requests')

def lambda_handler(event, context):
    try:
        request_id = event['pathParameters']['requestId']
        
        if not request_id:
            raise ValueError("RequestId is required.")
        
        table.delete_item(Key={'requestId': request_id})
        
        return {
            'statusCode': 200,
            'body': json.dumps('Request deleted successfully')
        }
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(str(e))
        }
    except (BotoCoreError, ClientError) as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error deleting request: {str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'An unexpected error occurred: {str(e)}')
        }
