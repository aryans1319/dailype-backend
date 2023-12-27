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
            return {"statusCode": 400, "body": json.dumps({"error": "Full name cannot be empty"})}
        
        if not re.match(r'^\d{10}$', mob_num):
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid mobile number format"})}
        
        if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan_num):
            return {"statusCode": 400, "body": json.dumps({"error": "Invalid PAN number format"})}

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

