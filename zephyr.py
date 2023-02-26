#!/usr/bin/env python3
from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/')
def index():
    message = "Automate all the things!"
    timestamp = int(time.time())
    data = {"message": message, "timestamp": timestamp}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

