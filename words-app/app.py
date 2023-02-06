import json
import os
import signal

from flask import Flask, jsonify, Request, render_template, request, url_for, redirect
from pymongo import MongoClient

from client import word_count_text

app = Flask(__name__)

# File System
FILE_SYSTEM = 'file_system'
JSON_FILE = 'total.json'
GLOBAL = 'global'
# mongodb
client = MongoClient('localhost', 27017)
db = client.flask_db
todos = db.todos
words = db.words
global_words_dict = db.global_words


def format_exception(exception: Exception):
    return jsonify({'error': str(exception)})


def get_txt_from_req():
    txt = request.args['txt']
    return txt


def update_global_dict_filesystem(res):
    with open(f'{FILE_SYSTEM}/{JSON_FILE}', 'r') as file:
        curr = json.load(file)
    global_dict = curr['global']
    for k, v in res.items():
        count = global_dict.get(k)
        global_dict[k] = (count + v if count else v)
        # else:
        #     global_dict[k] = v
    with open(f'{FILE_SYSTEM}/{JSON_FILE}', 'w+') as jf:
        json.dump(curr, jf)
    return curr


def update_text_counter_filesystem(res):
    with open(f'{FILE_SYSTEM}/{JSON_FILE}', 'r') as file:
        curr = json.load(file)
    curr['texts'].append(res)
    with open(f'{FILE_SYSTEM}/{JSON_FILE}', 'w+') as jf:
        json.dump(curr, jf)
    return


def update_json_file(res):
    update_text_counter_filesystem(res)
    global_dict = update_global_dict_filesystem(res)
    return global_dict


def update_txt_file(res):
    with open('total.txt', 'w') as tf:
        for k, v in res.items():
            tf.write(f"{k}:{v}")


def update_file_system(res):
    return update_json_file(res)


# End Points:

@app.route('/')
def welcome():
    return 'simple web app - welcome'


def update_global_dict_db(res):
    words_history = dict(global_words_dict.find())
    print(f"words_history: {words_history}")  # GET
    for k, v in res.items():
        count = words_history.get(k)
        print(f"count: {count}")
        words_history[k] = count + v if count else v

    global_words_dict.update_one("$set", words_history)


def get_global_word_counter_filesystem():
    with open(f'{FILE_SYSTEM}/{JSON_FILE}', 'r') as file:
        curr = json.load(file)
    return curr[GLOBAL]


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


# @app.route('/word_counter/', methods=(['POST']))
# def post_word_counter():
#     try:
#         txt = get_txt_from_req()
#         res = word_count_text(txt)
#         update_file_system(res)
#     except Exception as e:
#         return format_exception(e)
#     return f"{res}"


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
