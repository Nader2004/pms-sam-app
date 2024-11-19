import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tenants')

def lambda_handler(event, context):
    try:
        tenantId = event['pathParameters']['tenantId']
        
        if not tenantId:
            raise ValueError("Missing required path parameter: tenantId")

        table.delete_item(
            Key={
                'tenantId': tenantId
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Tenant deleted successfully')
        }
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(str(e))
        }
    except (BotoCoreError, ClientError) as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error deleting tenant: {str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'An unexpected error occurred: {str(e)}')
        }