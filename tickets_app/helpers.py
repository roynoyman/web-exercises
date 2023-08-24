from flask import request


def get_filter_params_from_request():
    filters = request.json
    title = filters.get('title') or None
    return title