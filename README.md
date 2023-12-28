![dailype_logo](https://github.com/aryans1319/dailype-backend/assets/72180855/66ed4533-d39a-4156-8e99-5513a6623410)
# Backend Task: Build a Serverless Function 
This repository contains AWS Lambda serverless functions that manage user data in a DynamoDB database. These functions support user creation, retrieval, retrieval of a single user, update user, and deletion operations.
Implemented all APIs and deployed on AWS

## Functions Overview

### 1. Create User [Done]

- **Endpoint:** `https://qo4xmoerdh.execute-api.us-east-1.amazonaws.com/create_user`
- **Method:** `POST`
- **Description:**
  - Accepts a JSON request body with keys:
    - `full_name` (String): User's full name
    - `mob_num` (String): User's mobile number
    - `pan_num` (String): User's PAN number
  - Validates input data:
    - `full_name`: Must not be empty
    - `mob_num`: Must be a valid 10-digit mobile number
    - `pan_num`: Must be a valid PAN number format (e.g., AABCP1234C)
  - Generates a unique `user_id` using UUID v4
  - Stores user data in DynamoDB against `user_id`
  - Returns a success message upon successful user creation
  - JSON Format
    ```
    {
      "full_name": "Aryan Shaw",
      "mob_num": "9876543210",
      "pan_num": "ABCDE1234F"
    }
### 2. Get All Users [Done] 

- **Endpoint:** `https://qo4xmoerdh.execute-api.us-east-1.amazonaws.com/get_users`
- **Method:** `GET`
- **Description:**
  - Retrieves all user records from the database
  - Returns a JSON object:
    - If users exist: `{ "users": [ { "user_id": "...", "full_name": "...", "mob_num": "...", "pan_num": "..." }, ... ] }`
    - If no users: `{ "users": [] }`

### 3. Get Single User [Done (Additional)]

- **Endpoint:** `https://qo4xmoerdh.execute-api.us-east-1.amazonaws.com/get_user?user_id=any_user_id`
- **Method:** `GET`
- **Description:**
  - Retrieves details of a single user based on `user_id`
  - Returns a JSON object with user details if found, else an error message

### 4. Delete User [Done]

- **Endpoint:** `https://m2shz41qnk.execute-api.us-east-1.amazonaws.com/dev/delete_user`
- **Method:** `DELETE`
- **Description:**
  - Accepts a JSON body with a `user_id` key
  - Checks if the `user_id` exists in the database
  - Deletes the user record if found, otherwise returns an error message
  - JSON Format
    ```
    {
      "user_id":"user_id_to_delete"
    }
### 5. Update User [Done]

- **Endpoint:** `https://m2shz41qnk.execute-api.us-east-1.amazonaws.com/dev/update_user`
- **Method:** `PUT`
- **Description:**
  - Accepts a JSON body with `user_id` and `update_data`
  - Checks if the provided `user_id` exists in the database
  - Updates user data based on `update_data`
  - Validates updated data fields similar to user creation
  - Returns a success message upon successful user update
  - JSON Format
    ```
    {
      "user_id": "id_to_be_updated",
      "update_data": {
          "full_name": "Updated Aryan",
          "mob_num": "1234567890",
          "pan_num": "HGSDM3553G"
        }
    }
## Deployed Endpoints 
| Functions | Deployed Link |
| --- | --- |
| Create User | [https://qo4xmoerdh.execute-api.us-east-1.amazonaws.com/create_user](https://qo4xmoerdh.execute-api.us-east-1.amazonaws.com/create_user) | 
| Get All Users | [https://qo4xmoerdh.execute-api.us-east-1.amazonaws.com/get_users](https://qo4xmoerdh.execute-api.us-east-1.amazonaws.com/get_users) |
| Get Single User |[https://qo4xmoerdh.execute-api.us-east-1.amazonaws.com/get_user?user_id=your_user_id](https://qo4xmoerdh.execute-api.us-east-1.amazonaws.com/get_user?user_id=your_user_id)  |
| Delete User |[https://m2shz41qnk.execute-api.us-east-1.amazonaws.com/dev/delete_user](https://m2shz41qnk.execute-api.us-east-1.amazonaws.com/dev/delete_user) |
| Update User |[https://m2shz41qnk.execute-api.us-east-1.amazonaws.com/dev/update_user](https://m2shz41qnk.execute-api.us-east-1.amazonaws.com/dev/update_user) |
    
## Services Used

- **AWS Services:**
  - Lambda
  - DynamoDB

## Tech Used
AWS Serverless Framework, DynamoDB, Python, AWS Lambda 

## Acknowledgement
Thank you for providing the task. I learned a lot about serverless framework starting from setting it up to integrating with the database and deployment on AWS and especially writing code in Python which was new to me but was fun to work with it, looking forward for the review and improvements

