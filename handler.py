import json
import boto3
import uuid
import re

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UsersTable')

def create_user(event, context):
    try:
        data = json.loads(event['body'])
        full_name = data['full_name']
        mob_num = data['mob_num']
        pan_num = data['pan_num']

        # Validation
        if not full_name:
            return {"statusCode": 400, "body": json.dumps({ "error": "Full name cannot be empty" })}
        
        if not re.match(r'^\d{10}$', mob_num):
            return {"statusCode": 400, "body": json.dumps({ "error": "Invalid mobile number format" })}
        
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan_num):
            return {"statusCode": 400, "body": json.dumps({ "error": "Invalid PAN number format" })}

        user_id = str(uuid.uuid4())

        # Store user data in DynamoDB
        table.put_item(Item={
            'user_id': user_id,
            'full_name': full_name,
            'mob_num': mob_num,
            'pan_num': pan_num
        })

        return {"statusCode": 200, "body": json.dumps({ "message": "User created successfully" })}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
        
def get_users(event, context):
    try:
        # Retrieve all user records from the DynamoDB table
        response = table.scan()
        items = response.get('Items', [])

        # If no users are found, return an empty list
        if not items:
            return {
                "statusCode": 200,
                "body": json.dumps({"users": []})
            }

        # Format user records according to specified structure
        users = [{
            "user_id": item['user_id'],
            "full_name": item['full_name'],
            "mob_num": item['mob_num'],
            "pan_num": item['pan_num']
        } for item in items]

        # Return a JSON object containing the user records
        return {
            "statusCode": 200,
            "body": json.dumps({
                "users": users
            })
        }

    except Exception as e:
        # Handle any exceptions and return an error response
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

def delete_user(event, context):
    try:
        data = json.loads(event['body'])
        user_id = data.get('user_id')

        # Check if user_id exists in the database
        response = table.get_item(Key={'user_id': user_id})
        if 'Item' not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "User not found!"})
            }

        # Delete user record from the database
        table.delete_item(Key={'user_id': user_id})

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "User deleted successfully"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

def update_user(event, context):
    try:
        data = json.loads(event['body'])
        user_id = data.get('user_id')
        update_data = data.get('update_data')

        # Check if user_id exists in the database
        response = table.get_item(Key={'user_id': user_id})
        if 'Item' not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "User not found with the provided user_id"})
            }

        # Extract and validate update_data
        full_name = update_data.get('full_name')
        mob_num = update_data.get('mob_num')
        pan_num = update_data.get('pan_num')

        # Validation for updated data
        if full_name and not full_name.strip():
            return {"statusCode": 400, "body": json.dumps({"error": "Full name cannot be empty"})}

        if mob_num and not re.match(r'^\d{10}$', mob_num):
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid mobile number format"})}

        if pan_num and not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan_num):
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid PAN number format"})}

        # Update user data in the database
        update_expression = 'SET '
        expression_attribute_values = {}

        if full_name:
            update_expression += 'full_name = :fn, '
            expression_attribute_values[':fn'] = full_name
        if mob_num:
            update_expression += 'mob_num = :mn, '
            expression_attribute_values[':mn'] = mob_num
        if pan_num:
            update_expression += 'pan_num = :pn, '
            expression_attribute_values[':pn'] = pan_num

        update_expression = update_expression.rstrip(', ')

        table.update_item(
            Key={'user_id': user_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "User updated successfully"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
