import time

from flask import request
from werkzeug.exceptions import UnsupportedMediaType

from ticket import TICKET_TEXT_ATTRIBUTES

TIMESTAMP_FILTERS = ['from', 'to']


def get_filter_params_from_request():
    if not request.headers.get('Content-Type') == 'application/json':
        return None
    filters = request.json
    # TODO: validate all filters
    # validate_filters(filters)
    text_filters = {k: v for k, v in filters.items() if k in TICKET_TEXT_ATTRIBUTES}

    timestamp_filters = {'from': filters.get('from') or 0, 'to': filters.get('from') or time.time()} if any(
        f in filters.keys() for f in TIMESTAMP_FILTERS) else None
    # except UnsupportedMediaType:
    #     return None
    return {'text_filters': text_filters, 'time_filters': timestamp_filters}
    # return {"title": title} if title else None
