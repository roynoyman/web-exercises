from flask import jsonify, request


def format_exception(exception: Exception):
    return jsonify({'error': str(exception)})


def get_args_from_req():
    return request.args


def validate_dict_filter(filter):
    if type(filter) != dict:
        raise TypeError(f"filter must be from type dict but {type(filter)} was passed")
