# -*- coding: utf-8 -*-

from flask import Flask, request
import mysql.connector
import os
import simplejson as json
from dotenv import load_dotenv
#load_dotenv()

IP = os.getenv('IP') or 'localhost'
PORT = os.getenv('PORT') or '5000'

DB_HOST = os.getenv('DB_HOST') or 'localhost' #con docker run
DB_USER = os.getenv('DB_USER') or 'myuser'
DB_PASSWORD = os.getenv('DB_PASSWORD') or 'myuser'
DB_NAME = os.getenv('DB_NAME') or 'db'

app = Flask(__name__)
mydb = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=3306,
)

@app.route('/', methods = ['GET'])
def index():
    if request.method == 'GET':
        return {'msg': 'Working'}
    
@app.route('/products', methods = ['GET'])
def get_products():
    if request.method == 'GET':
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM product")
        res = cursor.fetchall()
        print(res)
        return {'res': res}

if __name__ == '__main__':
    app.run(host=IP, port=PORT, debug=True)