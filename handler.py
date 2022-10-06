import boto3
import os
import base64
import eval_face_recognition

dynamodb = boto3.resource('dynamodb', 'us-east-1', aws_access_key_id = 'XXXXXXXXXXXXXXXXXXXXXXX', aws_secret_access_key='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
table = dynamodb.Table('Student_Data')

def fr_handler(event, context):
    key = event['name']
    inputimg = open('/tmp/' + key, "wb")
    inputimg.write(base64.b64decode(event['byte']))
    inputimg.close()
    
    # call the face recognition model in the file just downloaded
    val = eval_face_recognition.main('/tmp/' + key)
	
    # get details of the person recognized by face recognition model froom dynamoDB table
    response = table.get_item(
        Key={
                'name': val
            }
        )
    obj = []
    obj.append(response['Item']['name'])
    obj.append(response['Item']['major'])
    obj.append(response['Item']['year'])
    str_obj = str(obj).replace("'","")
    return str_obj
