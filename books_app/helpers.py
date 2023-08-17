import json
import random
import string

from flask import request


def decode_response(response):
    return json.loads(response.content.decode('utf-8'))


def generate_random_string(length=10):
    alphabet = string.ascii_letters
    return ''.join(random.choice(alphabet) for _ in range(length))


def get_args_from_req():
    return request.json
