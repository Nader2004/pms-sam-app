import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tenants')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        
        if 'tenantId' not in body or 'name' not in body or 'email' not in body or 'phone' not in body:
            raise ValueError("Missing required tenant attributes.")
        
        tenantId = body['tenantId']
        name = body['name']
        email = body['email']
        phone = body['phone']

        table.put_item(
            Item={
                'tenantId': tenantId,
                'name': name,
                'email': email,
                'phone': phone
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Tenant added successfully')
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
            'body': json.dumps(f'Error adding tenant: {str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'An unexpected error occurred: {str(e)}')
        }