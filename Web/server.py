from urllib2 import Request, urlopen
from flask import Flask, request, render_template, jsonify
import json
import os
from pprint import pprint
import search

def query_project(extra):
    imageList = search.searchImage(extra)
    return imageList
app = Flask(__name__)

@app.route('/')
def index():
    print "start"
    return render_template('index.html')

@app.route('/query')
def query():
    extra = request.args.get('extra', '', type=str)
    if(extra != ''):
        print extra
    data = json.dumps(query_project(extra))
    # print data
    print data
    return data

if __name__ == '__main__':
    app.run()