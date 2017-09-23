from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/sort', methods = ['POST'])
def sorting():
    if request.headers['Content-Type'] == 'application/json':
        requestJson = request.get_json()
        requestList = []
        for key in requestJson:
            requestList.append(requestJson[key])
        return requestList
    return 'NAK'

