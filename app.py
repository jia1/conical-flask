from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/sort', methods = ['POST'])
def sorting():
    if request.headers['Content-Type'] == 'application/json':
        data = request.data
        data.sort()
        return data
    return 'NAK'

