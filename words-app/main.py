import json

from flask import jsonify, request
from app import words, todos, global_words_dict

# File System
FILE_SYSTEM = 'file_system'
JSON_FILE = 'total.json'
GLOBAL = 'global'

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