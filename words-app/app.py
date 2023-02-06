import json
import os
import signal

from flask import Flask, jsonify, Request, render_template, request, url_for, redirect
from pymongo import MongoClient

from client import word_count_text

app = Flask(__name__)

# mongodb
client = MongoClient('localhost', 27017)
db = client.flask_db
todos = db.todos


def format_exception(exception: Exception):
    return jsonify({'error': str(exception)})


# End Points:

@app.route('/')
def welcome():
    return 'simple web app - welcome'


@app.route('/get_words_count/')
def get_words_count(txt=None):
    try:
        if not txt:
            txt = "bla bla bla aaa"
        res = word_count_text(txt)
    except TypeError as e:
        return format_exception(e)
    return f'count for text is: \n {res}'


def get_txt_from_req():
    txt = request.args['txt']
    return txt


def update_json_file(res):
    with open('file_system/total.json') as json_file:
        curr = json.load(json_file)
    print(f"curr: {curr}")
    for k, v in res.items():
        count = curr.get(k)
        if count:
            curr[k] = count + v
    print(curr)
    with open('file_system/total.json', 'w+') as jf:
        json.dump(curr, jf)


def update_txt_file(res):
    with open('total.txt', 'w') as tf:
        for k, v in res.items():
            tf.write(f"{k}:{v}")


def update_file_system(res):
    update_json_file(res)
    # update_txt_file(res)
    return


@app.route('/word_counter/', methods=(['POST']))
def post_word_counter():
    try:
        txt = get_txt_from_req()
        res = word_count_text(txt)
        update_file_system(res)
    except Exception as e:
        return format_exception(e)
    return f"{res}"


@app.route('/todo', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        content = request.args['content']
        # degree = request.args['degree']
        todos.insert_one({'content': content})
        return f"Done {content}"
    try:
        all_todos = todos.find()
    except Exception as e:
        return e
    rendered = render_template(all_todos)
    return f"good, {jsonify(rendered)}"


@app.route('/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({"success": True, "message": "Server is shutting down..."})
