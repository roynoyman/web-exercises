from abc import ABC

from database.db_helpers import extract_text_filters_from_filters, extract_timestamp_filters_from_filters, \
    is_text_filtered, \
    is_timestamp_filtered
from database.ticket import Ticket
from database.ticket_filter import Filter, TicketsFilter


class TicketsDataBase(ABC):
    def get_ticket_by_id(self, ticket_id):
        pass

    def get_all_tickets(self, filters=None) -> dict[str:Ticket]:
        pass

    def insert_ticket(self, ticket_id, ticket) -> None:
        pass


class SimpleTicketsDictDataBase(TicketsDataBase):
    db: dict
    ticket_filter: Filter

    def __init__(self):
        self.db = dict()
        self.ticket_filter = TicketsFilter()

    def get_ticket_by_id(self, ticket_id):
        return self.db.get(ticket_id)

    def get_all_tickets(self, filters=None) -> dict[str:Ticket]:
        if not filters:
            return self.db
        return self._get_tickets_with_filters(filters)

    def insert_ticket(self, ticket_id, ticket):
        self.db[ticket_id] = ticket

    def _get_tickets_with_filters(self, filters):
        # text_filters = extract_text_filters_from_filters(filters)
        # timestamp_filters = extract_timestamp_filters_from_filters(filters)
        tickets = {}
        for key, ticket in self.db.items():
            if self.ticket_filter.is_ticket_filtered(ticket=ticket, filters=filters):
                tickets[key] = ticket
            # if self._is_ticket_filtered(filters, ticket):
        return tickets

