import json
from random import choice
from string import ascii_letters, digits
import boto3
import datetime
import logging

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('AnnouncementTable')
x = datetime.datetime.now()

KEY_LEN = 20

API_VERSION = 1

def key_gen():
    keylist = [choice(ascii_letters+digits) for i in range(KEY_LEN)]
    return ("".join(keylist))

def lambda_handler(event, context):
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    try:
        if int(event['headers']['Api-Version']) != API_VERSION:
            return { "isBase64Encoded": True,
            "statusCode": 400,
            "headers": {},
            "body": "{\"message\":\"Invalid Api Version.\"}"
            }
    except Exception as e:
        logging.info(e)
        return { "isBase64Encoded": True,
        "statusCode": 400,
        "headers": {},
        "body": "{\"message\":\"Unable to fetch Api-Version.\"}"
        }
    
    body = json.loads(event['body'])
    
    try:
        table.put_item(Item={
                  'id': key_gen(),
                  'title': body['title'],
                  'description': body['desc'],
                  'date': x.strftime("%d")+"/"+x.strftime("%m")+"/"+x.strftime("%Y")
              })
    except Exception as e:
        logging.error(e)
        return { "isBase64Encoded": True,
        "statusCode": 500,
        "headers": {},
        "body": "{\"errorMessage\":\"Database Error. Announcement Not Saved.\"}"
        }
    return { 
        "isBase64Encoded": True, 
        "statusCode": 201, 
        "headers": {}, 
        "body": "{\"message\":\"Announcement Saved.\"}"
    }
