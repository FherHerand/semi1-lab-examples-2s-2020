import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

import base64
import tempfile
import uuid
import logging
import json

def lambda_handler(event, context):
    content = event
    name = content['name']
    ext = content['ext']
    b64_parts = content['base64'].split(',')
    image_64_encode_str = len(b64_parts) ==2 and b64_parts[1] or b64_parts[0]

    s3_client = boto3.client(
        's3',
    )

    BUCKET_NAME = 'bucket-test-201602822'
    FOLDER_NAME = 'images'
    file_name = '%s-%s.%s' % (name, uuid.uuid4(), ext)
    file_path = '%s/%s' % (FOLDER_NAME, file_name)
    image_64_encode = base64.b64decode((image_64_encode_str))
    f = tempfile.TemporaryFile()
    f.write(image_64_encode)
    f.seek(0)

    try:
        response = s3_client.put_object(Body=f, Bucket=BUCKET_NAME, Key=file_path, ACL='public-read')
        logging.info(response)
        return {
            'statusCode': 200,
            'body': response
        }
    except ClientError as e:
        logging.error(e)
        return {
            'statusCode': 500,
            'body': e.response
        }
