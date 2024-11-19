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

        table.delete_item(
            Key={
                'propertyId': propertyId
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Property deleted successfully')
        }
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(str(e))
        }
    except (BotoCoreError, ClientError) as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error deleting property: {str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'An unexpected error occurred: {str(e)}')
        }