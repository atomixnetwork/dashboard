from flask import Flask, render_template, request, jsonify, make_response
import json
import os

app = Flask(__name__)

LOG_KEY = "oCv4y7Q8rLVmIdevr4Vf"

@app.route('/applog')
def applog():
    if(request.args.get("accesskey") != None and request.args.get("accesskey") == LOG_KEY):
        if(os.path.exists('app.log') != True):
            response = app.response_class(
                response=json.dumps({"error": "Log file not found"}),
                status=404,
                mimetype="application/json",
            )
            return response
        else:
            f = open("app.log", "r")
            response = app.response_class(
                response=f.read(),
                status=200,
                mimetype='text/plain',
            )
            return response
    else:
        response = app.response_class(
            response=json.dumps({"error": "Invalid Access Key"}),
            status=403,
            mimetype="application/json",
        )
        return response

@app.route('/accesslog')
def accesslog():
    if(request.args.get("accesskey") != None and request.args.get("accesskey") == LOG_KEY):
        if(os.path.exists('app.log') != True):
            response = app.response_class(
                response=json.dumps({"error": "Log file not found"}),
                status=404,
                mimetype="application/json",
            )
            return response
        else:
            f = open("app.log", "r")
            response = app.response_class(
                response=f.read(),
                status=200,
                mimetype='text/plain',
            )
            return response
    else:
        response = app.response_class(
            response=json.dumps({"error": "Invalid Access Key"}),
            status=403,
            mimetype="application/json",
        )
        return response

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 8000, debug=True)
