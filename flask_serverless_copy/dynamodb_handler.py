
import boto3 
from botocore.exceptions import ClientError
from sqlalchemy import false
from datetime import datetime
from flask import request

client = ddb = boto3.client('dynamodb', 
                endpoint_url='http://localhost:8000',
                region_name="dummy", 
                aws_access_key_id="dummy",
                aws_secret_access_key="dummy")

resource = boto3.resource('dynamodb', 
                    endpoint_url='http://localhost:8000',
                    region_name="dummy", 
                    aws_access_key_id="dummy",
                    aws_secret_access_key="dummy")




def deleteTables(table):
    try:
        client.delete_table(TableName=table)

    except ClientError as ce:
        if ce.response['Error']['Code'] == 'ResourceNotFoundException':
            print ("Table does not exist. Create the table first and try again.")
        else:
            print ("Unknown exception occurred while querying for the table. Printing full error:")
            print(ce.response)
            


def createTableTodo(table):
    try:
            ddb.create_table(
                    TableName=table,
                    AttributeDefinitions=[{
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                }],
                KeySchema=[{
                    'AttributeName': 'id',
                    'KeyType': 'HASH' 
                }],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }

            )
            print("Table creation success")
    except ClientError as ce:
            if ce.response['Error']['Code'] == 'ResourceInUseException':
                print ("Cannot create preexisting table")
            else:
                print ("Unknown exception occurred while querying for the table. Printing full error:")
                print(ce.response)

TodoTable = resource.Table('Todo')
User = resource.Table('User')

def AddItemToTodo(id, description, due_date, completed):
    response = TodoTable.put_item(
        Item = {
            'id': id,
            'description'  : description,
            'completed' : completed,
            'due_date'  : due_date
        }
    )
    return response


def GetTodoItem(id):
    response = TodoTable.get_item(
        Key = {
            'id': id
        },
        AttributesToGet=[
            'id', 'description',
            'completed', 'false'
        ]
    )
    return response    

# GetTodoItem(5)

def UpdateTodoItem(id, data:dict):
    response = TodoTable.update_item(
        Key={
            'id': id
        },
        AttributesUpdates={
            'description': {
                'Value': data['description'],
                'Action': 'PUT'
            },
            'author': {
                'Value'  : data['completed'],
                'Action' : 'PUT'
            },
            'due_date': {
                'Value'  : data['due_date'],
                'Action' : 'PUT' 
            }
        },
        ReturnValues = "UPDATED_NEW"
    )
    return response


def DeleteTodoItem(id):
    response = TodoTable.delete_item(
        Key = {
            'id': id
        }
    )
    return response





