import time

from api.helpers import TIMESTAMP_FILTERS
from database.ticket import TICKET_TEXT_ATTRIBUTES


def extract_text_filters_from_filters(filters):
    filter_keys = filters.keys()
    text_filters = {key: filters.get(key) for key in TICKET_TEXT_ATTRIBUTES if key in filter_keys} or None
    return text_filters


def extract_timestamp_filters_from_filters(filters):
    filter_keys = filters.keys()
    timestamp_filters = {'from': filters.get('from') or 0, 'to': filters.get('to') or time.time()} if any(
        timestamp_filter in filter_keys for timestamp_filter in TIMESTAMP_FILTERS) else None
    return timestamp_filters


def is_text_filtered(text_filters, ticket):
    return all(getattr(ticket, field) == value for field, value in text_filters.items())


def is_timestamp_filtered(timestamp_filters, ticket):
    return timestamp_filters['from'] <= ticket.creationTime <= timestamp_filters['to']
