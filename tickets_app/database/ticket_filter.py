from abc import ABC, abstractmethod

from database.db_helpers import extract_text_filters_from_filters, extract_timestamp_filters_from_filters
from database.ticket import Ticket


class Filter(ABC):
    # ticekt_schema: Ticket

    @abstractmethod
    def is_ticket_filtered(self, ticket, filters):
        pass

    @staticmethod
    def is_text_filtered(ticket, text_filters):
        pass

    @staticmethod
    def is_timestamp_filter(ticket, timestamp_filters):
        pass


class TicketsFilter(Filter):
    def is_ticket_filtered(self, ticket, filters):
        text_filters = extract_text_filters_from_filters(filters)
        timestamp_filters = extract_timestamp_filters_from_filters(filters)
        is_text_filter = self.is_text_filtered(ticket, text_filters) if text_filters else True
        is_timestamp_filter = self.is_timestamp_filtered(ticket, timestamp_filters) if timestamp_filters else True
        return is_text_filter and is_timestamp_filter

    @staticmethod
    def is_text_filtered(ticket, text_filters):
        return all(getattr(ticket, field) == value for field, value in text_filters.items())

    @staticmethod
    def is_timestamp_filtered(ticket, timestamp_filters):
        return timestamp_filters['from'] <= ticket.creationTime <= timestamp_filters['to']
