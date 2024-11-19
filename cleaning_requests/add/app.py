import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cleaning_service_requests')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        
        required_fields = ['tenantId', 'requestId', 'propertyId', 'requestDate', 'status', 'details']
        for field in required_fields:
            if field not in body:
                raise ValueError(f"Missing required field: {field}")
        
        table.put_item(Item=body)

        return {
            'statusCode': 200,
            'body': json.dumps('Cleaning service request added successfully')
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid JSON format')
        }
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(str(e))
        }
    except (BotoCoreError, ClientError) as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error adding request: {str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'An unexpected error occurred: {str(e)}')
        }