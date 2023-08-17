from flask import jsonify
from requests import HTTPError


class ItemNotExist(HTTPError):
    def __str__(self):
        return 'Item not exist in DB'

def format_exception(exception: Exception):
    return jsonify({'error': str(exception)})