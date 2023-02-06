import json
import os
import signal
from main import get_txt_from_req, update_global_dict_db, format_exception
from flask import Flask, jsonify, Request, render_template, request, url_for, redirect
from pymongo import MongoClient

from client import word_count_text

app = Flask(__name__)

# mongodb
client = MongoClient('localhost', 27017)
db = client.flask_db
todos = db.todos
words = db.words
global_words_dict = db.global_words



# End Points:

@app.route('/')
def welcome():
    return 'simple web app - welcome'




@app.route('/update_word', methods=(["POST"]))
def update_word():
    txt = get_txt_from_req()
    words.insert_one({"txts:": [txt]})
    return "200"


@app.route('/update_word_current', methods=(["POST"]))
def update_word_current():
    txt = get_txt_from_req()
    counter = word_count_text(txt)
    all_words = list(words.find({}))
    globals_dict = all_words[0]['globals']
    for k, v in counter.items():
        count = globals_dict.get(k)
        globals_dict[k] = count + v if count else v
    id = all_words[0]['_id']
    # all_words[0]['globals']['bla'] = 10
    words.update_one({'_id': id}, {"$set": all_words[0]})

    return f"Updated global: {all_words[0]['globals']}"


@app.route('/word_counter', methods=(['GET', 'POST']))
def get_history_counter():
    if request.method == 'POST':
        txt = get_txt_from_req()
        res = word_count_text(txt)
        words.insert_one({'counter': res})
        # updated_global_dict = update_file_system(res)
        updated_global_dict = update_global_dict_db(res)
        return jsonify({"msg": f"text was inserted, updated global dict: {updated_global_dict}"}), 201
    try:
        # global_dict = get_global_word_counter_filesystem()
        words_history = list(words.find({}))
    except Exception as e:
        return e
    return f"Words: {words_history}"


@app.route('/words_count/')
def get_words_count(txt=None):
    try:
        if not txt:
            txt = "bla bla bla aaa"
        res = word_count_text(txt)
    except TypeError as e:
        return format_exception(e)
    return f'count for text is: \n {res}'


@app.route('/todo', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        content = request.args['content']
        todos.insert_one({'content': content})
        return f"Done {content}"
    try:
        all_todos = list(todos.find({}))
    except Exception as e:
        return e
    return f"TDOOS: {all_todos}"


@app.route('/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({"success": True, "message": "Server is shutting down..."})
