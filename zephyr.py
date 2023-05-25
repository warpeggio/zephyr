#!/usr/bin/env python3
import sys
import time
import json
import random
import time
import boto3

from flask import Flask, jsonify

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('zephyrTable')

argv  = sys.argv[0:]
stack = argv[1]

app = Flask(__name__)

@app.route('/')
def index():
    message = "Technology and tools don't solve problems, people do"
    timestamp = int(time.time())
    data = {"message": message, "timestamp": timestamp}
    
    struct_time = time.gmtime()        
    item = {
        'Id': timestamp,
        'Year': struct_time.tm_year,
        'Month': struct_time.tm_mon,
        'Day': struct_time.tm_mday,
        'Hour': struct_time.tm_hour,
        'Minute': struct_time.tm_min,
        'Second': struct_time.tm_sec,
        'Weekday': struct_time.tm_wday,
        'YearDay': struct_time.tm_yday,
        'IsDst': struct_time.tm_isdst
    }
    table.put_item(Item=item)

    return jsonify(data)

@app.route('/healthz')
def health_check():
    return "OK", 200

@app.route('/readyz')
def ready_check():
    # We need to generate some noise for the logs. This 20% chance of failure for a node
    # should generate that. 20% will keep the odds of all three nodes going offline together
    # below 1%.
    rand_num = random.randint(1, 5)
    if rand_num == 1:
        return "Error", 500
    else:
        return "OK", 200

def test_response_is_json():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    json.loads(response.get_data())

def test_message_is_automate():
    response = app.test_client().get('/')
    data = json.loads(response.get_data())
    assert data['message'] == "Automate all the things!"

if __name__ == '__main__':
    app.run(host="0.0.0.0")

