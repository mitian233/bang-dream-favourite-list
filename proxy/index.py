from flask import Flask, request, send_file
import json, requests, io

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False  # json出力のソートを無効化

def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return resp

@app.route('/')
def hello_world():  # put application's code here
    returnData = json.loads('{"message": "Hello World"}')
    if request.args.get('name'):
        returnData['message'] = "Hello " + request.args.get('name')
    return returnData

if __name__ == '__main__':
    app.run()