from flask import Flask, jsonify
from client import word_count_text

app = Flask(__name__)


def format_exception(exception: Exception):
    return jsonify({'error': str(exception)})


@app.route('/')
def welcome():
    return 'simple web app - welcome'


@app.route('/get_words_count')
def get_words_count():
    try:
        res = word_count_text("bla bla bla aaa")
    except TypeError as e:
        return format_exception(e)
    return f'count for text is: \n {res}'

