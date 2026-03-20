# Setup - How the code talks to AWS Services.  Connect to DynamoDB and grab reference from Todos table.
import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Todos')


# Entry point - How API Gateway forwards the request to this function.
def lambda_handler(event, context):
    method = event.get('httpMethod')

    # The Router - One Lambda that checks the HTTP method and calls the appropriate function.
    try:
        if method == 'GET':
            return get_todos()
        elif method == 'POST':
            body = json.loads(event.get('body', '{}'))
            return create_todo(body)
        elif method == 'PUT':
            body = json.loads(event.get('body', '{}'))
            return update_todo(body)
        elif method == 'DELETE':
            body = json.loads(event.get('body', '{}'))
            return delete_todo(body)
        else:
            return response(400, {'error': f'Unsupported method: {method}'})
    except Exception as e:
        return response(500, {'error': str(e)})
     

# Read - Returns every item in the table.
def get_todos():
    result = table.scan()
    items = result.get('Items', [])
    return response(200, items)


# Creatation - Generates random UID as the ID, sets completed to false, and then writes to DynamoDB wit put_item.
def create_todo(body):
    task = body.get('task')
    if not task:
        return response(400, {'error': 'Task is required'})

    item = {
        'id': str(uuid.uuid4()),
        'task': task,
        'completed': False,
        'createdAt': datetime.utcnow().isoformat()
    }
    table.put_item(Item=item)
    return response(201, item)


# Update - 
def update_todo(body):
    todo_id = body.get('id')
    if not todo_id:
        return response(400, {'error': 'ID is required'})

    completed = body.get('completed', True)
    task = body.get('task')

    update_expr = 'SET completed = :c'
    expr_values = {':c': completed}

    if task: 
        update_expr += ', task = :t'
        expr_values[':t'] = task


    result = table.update_item(
        Key={'id': todo_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_values,
        ReturnValues='ALL_NEW'
    )
    return response(200, result.get('Attributes'))

# Delete - Find item by it's partition key and remove it
def delete_todo(body):
    todo_id = body.get('id')
    if not todo_id:
        return response(400, {'error': 'ID is required'})

    table.delete_item(Key={'id': todo_id})
    return response(200, {'message': 'Todo deleted'})

# Response Helper - Return JSON and allow cross-origin requests.
def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body)
    }

