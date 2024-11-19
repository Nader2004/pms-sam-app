import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('properties')

def lambda_handler(event, context):
    try:
        propertyId = event['pathParameters']['propertyId']
        
        if not propertyId:
            raise ValueError("Missing required path parameter: propertyId")

        response = table.get_item(
            Key={
                'propertyId': propertyId
            }
        )

        item = response.get('Item')

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps('Property not found')
            }

        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(str(e))
        }
    except (BotoCoreError, ClientError) as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error retrieving property: {str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'An unexpected error occurred: {str(e)}')
        }