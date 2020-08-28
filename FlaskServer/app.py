# -*- coding: utf-8 -*-

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from flask import Flask, request

import base64
import tempfile
import uuid
import logging
import creds

app = Flask(__name__)

@app.route('/s3/upload', methods = ['POST'])
def s3_upload():
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
            return response
        except ClientError as e:
            logging.error(e)
            return e.response

@app.route('/ddb/person/save', methods = ['POST'])
def ddb_save():
    if request.method == 'POST':
        content = request.get_json()
        id = content['id']
        name = content['name']

        dynamodb_client = boto3.client(
            'dynamodb',
            aws_access_key_id=creds.dynamodb['access_key_id'],
            aws_secret_access_key=creds.dynamodb['secret_access_key'],
            region_name=creds.dynamodb['region'],
        )

        try:
            response = dynamodb_client.put_item(
                TableName='test',
                Item={
                    'id': {'S': id},
                    'name': {'S': name},
                    'courses': {'L': []}
                },
            )
            logging.info(response)
            return response
        except ClientError as e:
            logging.error(e)
            return e.response

@app.route('/ddb/courses/update', methods = ['PUT'])
def ddb_update():
    if request.method == 'PUT':
        content = request.get_json()
        id = content['id']
        course_code = content['course_code']
        course_name = content['course_name']

        dynamodb_client = boto3.client(
            'dynamodb',
            aws_access_key_id=creds.dynamodb['access_key_id'],
            aws_secret_access_key=creds.dynamodb['secret_access_key'],
            region_name=creds.dynamodb['region'],
        )

        try:
            response = dynamodb_client.update_item(
                TableName='test',
                Key={'id': {'S': id}},
                UpdateExpression='SET #courses = list_append(#courses, :new_course)',
                ExpressionAttributeNames={
                    '#courses': 'courses',
                },
                ExpressionAttributeValues={
                    ':new_course': {
                        'L': [
                            {
                                'M': {
                                    'code': {'S': course_code},
                                    'name': {'S': course_name},
                                }
                            }
                        ]
                    }
                },
                ReturnValues='UPDATED_NEW',
            )
            logging.info(response)
            return response
        except ClientError as e:
            logging.error(e)
            return e.response

@app.route('/ddb/person/query', methods = ['GET'])
def ddb_query():
    if request.method == 'GET':
        content = request.args
        name = content['name']

        dynamodb_client = boto3.client(
            'dynamodb',
            aws_access_key_id=creds.dynamodb['access_key_id'],
            aws_secret_access_key=creds.dynamodb['secret_access_key'],
            region_name=creds.dynamodb['region'],
        )

        try:
            response = dynamodb_client.scan(
                TableName='test',
                #ProjectionExpression='courses',
                FilterExpression='#name = :my_name',
                ExpressionAttributeNames={
                    '#name': 'name',
                },
                ExpressionAttributeValues={
                    ':my_name': {'S': name},
                }
            )
            logging.info(response)
            return response
        except ClientError as e:
            logging.error(e)
            return e.response

@app.route('/rek/compare', methods = ['POST'])
def rek_compare():
    if request.method == 'POST':
        content = request.get_json()
        source_image_name = content['source_image_name']
        target_image_name = content['target_image_name']

        rekognition_client = boto3.client(
            'rekognition',
            aws_access_key_id=creds.rekognition['access_key_id'],
            aws_secret_access_key=creds.rekognition['secret_access_key'],
            region_name=creds.rekognition['region'],
        )

        BUCKET_NAME = 'bucket-test-201602822'
        FOLDER_NAME = 'images'
        source_image_path = '%s/%s' % (FOLDER_NAME, source_image_name)
        target_image_path = '%s/%s' % (FOLDER_NAME, target_image_name)

        try:
            response = rekognition_client.compare_faces(
                SourceImage={
                    'S3Object': {
                        'Bucket': BUCKET_NAME,
                        'Name': source_image_path,
                    }
                },
                TargetImage={
                    'S3Object': {
                        'Bucket': BUCKET_NAME,
                        'Name': target_image_path,
                    }
                },
                SimilarityThreshold=90,
            )
            logging.info(response)
            return response
        except ClientError as e:
            logging.error(e)
            return e.response

@app.route('/rek/labels', methods = ['GET'])
def rek_labels():
    if request.method == 'GET':
        content = request.args
        source_image_name = content['image_name']

        rekognition_client = boto3.client(
            'rekognition',
            aws_access_key_id=creds.rekognition['access_key_id'],
            aws_secret_access_key=creds.rekognition['secret_access_key'],
            region_name=creds.rekognition['region'],
        )

        BUCKET_NAME = 'bucket-test-201602822'
        FOLDER_NAME = 'images'
        image_path = '%s/%s' % (FOLDER_NAME, source_image_name)

        try:
            response = rekognition_client.detect_labels(
                Image={
                    'S3Object': {
                        'Bucket': BUCKET_NAME,
                        'Name': image_path,
                    }
                },
                #MaxLabels=1,
                #MinConfidence=50,
            )
            logging.info(response)
            return response
        except ClientError as e:
            logging.error(e)
            return e.response

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)