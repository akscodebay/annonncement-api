import json
import boto3
import logging

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('AnnouncementTable')

API_VERSION = 1

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
    try:
        pageNo = int(event['queryStringParameters']['pageNo'])
    except Exception as e:
        logging.info(e)
        return { "isBase64Encoded": True,
        "statusCode": 400,
        "headers": {},
        "body": "{\"errorMessage\":\"Unable to fetch Page Number.\"}"
        }
    
    try:
        response = table.scan(Limit=10)
        if response['Count'] == 0:
            return { "isBase64Encoded": True,
            "statusCode": 204,
            "headers": {}
            }
        pageNo-=1
        
        if pageNo > 0:
            while 'LastEvaluatedKey' in response:
                key = response['LastEvaluatedKey']
                response = table.scan(Limit=10, ExclusiveStartKey=key)
                pageNo-=1
                if pageNo == 0:
                    break
                
        if pageNo > 0:
            return { "isBase64Encoded": True,
            "statusCode": 204,
            "headers": {}
            }
        else:
            return { "isBase64Encoded": True,
            "statusCode": 200,
            "headers": {},
            "body": "{'Items:'"+ json.dumps(response['Items']) +"}"
            }
    except Exception as e:
        logging.error(e)
        return { "isBase64Encoded": True,
        "statusCode": 500,
        "headers": {},
        "body": "{\"errorMessage\":\"Something went Wrong.\"}"
        }
    
    