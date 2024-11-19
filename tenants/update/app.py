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
        update_expression = "SET #n = :n, email = :e, phone = :p"
        expression_attribute_names = {
            '#n': 'name'
        }
        expression_attribute_values = {
            ':n': body['name'],
            ':e': body['email'],
            ':p': body['phone']
        }

        table.update_item(
            Key={
                'tenantId': tenantId
            },
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Tenant updated successfully')
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
            'body': json.dumps(f'Error updating tenant: {str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'An unexpected error occurred: {str(e)}')
        }