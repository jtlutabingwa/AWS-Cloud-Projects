# Serverless To-Do List API
 
Built a fully serverless REST API on AWS using Lambda, API Gateway, and DynamoDB. No servers to manage — requests come in through API Gateway, trigger a Python Lambda function, and read/write to a DynamoDB table.
 
## Overview
 
| | |
|---|---|
| **Services Used** | Lambda, API Gateway, DynamoDB, IAM |
| **Runtime** | Python 3.12 |
| **Endpoints** | GET, POST, PUT, DELETE |
| **Cost** | Free Tier eligible |
 
## Architecture
 
```
Client (Postman/curl)
     │
     │  HTTPS
     ▼
┌──────────────────┐
│   API Gateway    │
│                  │
│  GET    /todos   │  → List all to-dos
│  POST   /todos   │  → Create a to-do
│  PUT    /todos   │  → Update a to-do
│  DELETE /todos   │  → Delete a to-do
└────────┬─────────┘
         ▼
┌──────────────────┐
│  Lambda Function │
│  (Python 3.12)   │
└────────┬─────────┘
         ▼
┌──────────────────┐
│  DynamoDB Table  │
│  (Todos)         │
└──────────────────┘
```
 
## What I Did
 
### Created the DynamoDB Table
 
Set up a `Todos` table with `id` (String) as the partition key and on-demand capacity mode.
 
<img src="images/01-dynamodb-table.png" alt="DynamoDB Table" width="600">
 
### Created an IAM Role for Lambda
 
Created `lambda-todo-role` with `AmazonDynamoDBFullAccess` and `AWSLambdaBasicExecutionRole` policies so the Lambda function has permission to read/write to DynamoDB and log to CloudWatch.
 
<img src="images/02-iam-role-setup.png" alt="IAM Role Setup" width="600">
 
<img src="images/03-iam-role-review.png" alt="IAM Role Review" width="600">
 
<img src="images/04-iam-role-created.png" alt="IAM Role Created" width="600">
 
### Wrote the Lambda Function
 
Single Python function that handles all four CRUD operations based on the HTTP method. The code is in [`lambda_function.py`](lambda_function.py).
 
Key things it does:
- Routes requests by checking `event['httpMethod']`
- Generates UUIDs for new to-do items
- Uses DynamoDB's `UpdateExpression` syntax for partial updates
- Returns consistent JSON responses with CORS headers
 
### Set Up API Gateway
 
Created a REST API with a `/todos` resource and wired up GET, POST, PUT, and DELETE methods — all pointing to the same Lambda function with Lambda Proxy Integration enabled.
 
<img src="images/05-api-gateway-resource.png" alt="API Gateway Resource" width="600">
 
<img src="images/06-api-gateway-method.png" alt="API Gateway Method Detail" width="600">
 
<img src="images/07-api-gateway-methods.png" alt="API Gateway All Methods" width="600">
 
### Tested with Postman
 
All four operations are working:
 
**POST** — Create a new to-do (201 Created):
 
<img src="images/10-postman-post.png" alt="POST - Create Todo" width="600">
 
**GET** — List all to-dos (200 OK):
 
<img src="images/11-postman-get.png" alt="GET - List Todos" width="600">
 
**PUT** — Mark a to-do as completed (200 OK):
 
<img src="images/08-postman-put.png" alt="PUT - Update Todo" width="600">
 
**DELETE** — Remove a to-do (200 OK):
 
<img src="images/09-postman-delete.png" alt="DELETE - Remove Todo" width="600">
 
## What I Learned
 
- How serverless architecture works — Lambda only runs when triggered, no idle servers
- API Gateway maps HTTP routes to Lambda and handles the public HTTPS endpoint
- DynamoDB is schema-less beyond the partition key, which makes it flexible for simple data
- IAM roles are how AWS services get permission to talk to each other
- Lambda Proxy Integration is required for API Gateway to pass the full HTTP request (method, body, headers) to Lambda
- The "Missing Authentication Token" error from API Gateway actually means the route doesn't exist, not an auth issue
