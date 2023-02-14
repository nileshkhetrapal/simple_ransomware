from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
    
def store_data():
    # This function can remain the same
    data = request.get_json()
    with open('/var/www/html/data.txt', 'a') as f:
        f.write(str(data) + '\n')
    return "Data stored successfully"

