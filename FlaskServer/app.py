# -*- coding: utf-8 -*-

import boto3
from botocore.exceptions import ClientError
from flask import Flask, request

import base64
import tempfile
import uuid
import logging
import creds

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/upload', methods = ['POST'])
def upload():
    if request.method == 'POST':
        content = request.get_json()
        name = content['name']
        ext = content['ext']
        b64_parts = content['base64'].split(',')
        image_64_encode_str = len(b64_parts) ==2 and b64_parts[1] or b64_parts[0]

        s3_client = boto3.client(
            's3',
            aws_access_key_id=creds.s3['access_key_id'],
            aws_secret_access_key=creds.s3['secret_access_key'],
        )

        BUCKET_NAME = 'test-test-semi1'
        FOLDER_NAME = 'general'
        file_name = '%s-%s.%s' % (name, uuid.uuid4(), ext)
        file_path = '%s/%s' % (FOLDER_NAME, file_name)
        image_64_encode = base64.b64decode((image_64_encode_str))
        f = tempfile.TemporaryFile()
        f.write(image_64_encode)
        f.seek(0)

        try:
            response = s3_client.put_object(Body=f, Bucket=BUCKET_NAME, Key=file_path, ACL='public-read')
            logging.info(response)
        except ClientError as e:
            logging.error(e)
            return 'Error'
        return response
        

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)