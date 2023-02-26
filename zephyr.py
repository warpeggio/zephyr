#!/usr/bin/env python3
import time
import json

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    message = "Automate all the things!"
    timestamp = int(time.time())
    data = {"message": message, "timestamp": timestamp}
    return jsonify(data)

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

