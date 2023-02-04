import json

from flask import Flask, jsonify, Request, request
from client import word_count_text

app = Flask(__name__)


def format_exception(exception: Exception):
    return jsonify({'error': str(exception)})


# End Points:

@app.route('/')
def welcome():
    return 'simple web app - welcome'


@app.route('/get_words_count/<user_id>')
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
    with open('total.json', 'w') as jf:
        json.dump(res, jf)


def update_txt_file(res):
    with open('total.txt', 'w') as tf:
        for k, v in res.items():
            tf.write(f"{k}:{v}")


def update_file_system(res):
    update_json_file(res)
    update_txt_file(res)
    return


@app.route('/word_counter/', methods=(['POST']))
def post_word_counter():
    try:
        txt = get_txt_from_req()
        res = get_words_count(txt)
        update_file_system(res)
    except Exception as e:
        return format_exception(e)
    return 200
