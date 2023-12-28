import json
import boto3
import uuid
import re

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UsersTable')

def validate_mobile_number(mob_num):
    return bool(re.match(r'^\d{10}$', mob_num))

def validate_pan_number(pan_num):
    return bool(re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan_num))

def validate_input(full_name, mob_num, pan_num):
    if not full_name.strip():
        return False, "Full name cannot be empty"
    if not validate_mobile_number(mob_num):
        return False, "Invalid mobile number format"
    if not validate_pan_number(pan_num):
        return False, "Invalid PAN number format"
    return True, None

def create_user(event, context):
    try:
        data = json.loads(event['body'])
        full_name = data.get('full_name')
        mob_num = data.get('mob_num')
        pan_num = data.get('pan_num')

        is_valid, validation_error = validate_input(full_name, mob_num, pan_num)
        if not is_valid:
            return {"statusCode": 400, "body": json.dumps({"error": validation_error})}

        user_id = str(uuid.uuid4())

        # Store user data in DynamoDB
        table.put_item(Item={
            'user_id': user_id,
            'full_name': full_name,
            'mob_num': mob_num,
            'pan_num': pan_num
        })

        return {"statusCode": 200, "body": json.dumps({"message": "User created successfully"})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

def get_users(event, context):
    try:
        # Retrieve all user records from the DynamoDB table
        response = table.scan()
        items = response.get('Items', [])

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
            "body": json.dumps({"users": users})
        }

    except Exception as e:
        # Handle any exceptions and return an error response
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

def get_single_user(event, context):
    try:
        user_id = event.get('queryStringParameters', {}).get('user_id')

        if not user_id:
            return {"statusCode": 400, "body": json.dumps({"error": "User ID is required"})}

        response = table.get_item(Key={'user_id': user_id})
        user_data = response.get('Item')

        if not user_data:
            return {"statusCode": 404, "body": json.dumps({"error": "User not found with the provided user_id"})}

        user_details = {
            "user_id": user_data['user_id'],
            "full_name": user_data['full_name'],
            "mob_num": user_data['mob_num'],
            "pan_num": user_data['pan_num']
        }

        return {"statusCode": 200, "body": json.dumps(user_details)}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

def delete_user(event, context):
    try:
        data = json.loads(event['body'])
        user_id = data.get('user_id')

        response = table.get_item(Key={'user_id': user_id})
        if 'Item' not in response:
            return {"statusCode": 404, "body": json.dumps({"error": "User not found!"})}

        table.delete_item(Key={'user_id': user_id})

        return {"statusCode": 200, "body": json.dumps({"message": "User deleted successfully"})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

def update_user(event, context):
    try:
        data = json.loads(event['body'])
        user_id = data.get('user_id')
        update_data = data.get('update_data', {})

        response = table.get_item(Key={'user_id': user_id})
        if 'Item' not in response:
            return {"statusCode": 404, "body": json.dumps({"error": "User not found with the provided user_id"})}

        full_name = update_data.get('full_name')
        mob_num = update_data.get('mob_num')
        pan_num = update_data.get('pan_num')

        if full_name is not None and not full_name.strip():
            return {"statusCode": 400, "body": json.dumps({"error": "Full name cannot be empty"})}

        if mob_num is not None and not validate_mobile_number(mob_num):
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid mobile number format"})}

        if pan_num is not None and not validate_pan_number(pan_num):
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid PAN number format"})}

        update_expression = 'SET '
        expression_attribute_values = {}

        if full_name is not None:
            update_expression += 'full_name = :fn, '
            expression_attribute_values[':fn'] = full_name
        if mob_num is not None:
            update_expression += 'mob_num = :mn, '
            expression_attribute_values[':mn'] = mob_num
        if pan_num is not None:
            update_expression += 'pan_num = :pn, '
            expression_attribute_values[':pn'] = pan_num

        update_expression = update_expression.rstrip(', ')

        table.update_item(
            Key={'user_id': user_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )

        return {"statusCode": 200, "body": json.dumps({"message": "User updated successfully"})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

