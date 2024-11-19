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
        update_expression = "SET #n = :n, address = :a, occupied = :o"
        expression_attribute_names = {
            '#n': 'name'
        }
        expression_attribute_values = {
            ':n': body['name'],
            ':a': body['address'],
            ':o': body['occupied']
        }

        table.update_item(
            Key={
                'propertyId': propertyId
            },
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Property updated successfully')
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
            'body': json.dumps(f'Error updating property: {str(e)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'An unexpected error occurred: {str(e)}')
        }