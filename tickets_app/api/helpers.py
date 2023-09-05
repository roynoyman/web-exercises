from flask import request

from api.exceptions import NotSupportedFilters
from database.ticket import TICKET_TEXT_ATTRIBUTES

TIMESTAMP_FILTERS = ['from', 'to']


def validate_filter_keys(filters: list) -> bool:
    valid_filters = all(
        filter_value in TIMESTAMP_FILTERS or filter_value in TICKET_TEXT_ATTRIBUTES for filter_value in filters)
    if not valid_filters:
        raise NotSupportedFilters(
            f'Some filters are not supported. \n The supported filters are: timestamp filters: {TIMESTAMP_FILTERS} or text_filters: {TICKET_TEXT_ATTRIBUTES}')
    return valid_filters


def get_filter_params_from_request():
    if not request.headers.get('Content-Type') == 'application/json':
        return None
    filters = request.json
    validate_filter_keys(filters.keys())
    return filters
