import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('properties')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        
        if 'propertyId' not in body or 'name' not in body or 'address' not in body or 'occupied' not in body:
            raise ValueError("Missing required property attributes.")
        
        propertyId = body['propertyId']
        name = body['name']
        address = body['address']
        occupied = body['occupied']

        table.put_item(
            Item={
                'propertyId': propertyId,
                'name': name,
                'address': address,
                'occupied': occupied
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Property added successfully')
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
            'body': json.dumps(f'Error adding property: {str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'An unexpected error occurred: {str(e)}')
        }