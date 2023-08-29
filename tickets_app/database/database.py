from database.db_helpers import extract_text_filters_from_filters, extract_timestamp_filters_from_filters, is_text_filtered, \
    is_timestamp_filtered
from database.ticket import Ticket


class TicketsDataBase:
    def get_ticket_by_id(self, ticket_id):
        pass

    def get_all_tickets(self, filters=None) -> dict[str:Ticket]:
        pass

    def insert_ticket(self, ticket_id, ticket) -> None:
        pass


class SimpleTicketsDictDataBase(TicketsDataBase):
    db: dict

    def __init__(self):
        self.db = dict()

    def get_ticket_by_id(self, ticket_id):
        return self.db.get(ticket_id)

    def get_all_tickets(self, filters=None) -> dict[str:Ticket]:
        if not filters:
            return self.db
        return self._get_tickets_with_filters(filters)

    def insert_ticket(self, ticket_id, ticket):
        self.db[ticket_id] = ticket

    def _get_tickets_with_filters(self, filters):
        text_filters = extract_text_filters_from_filters(filters)
        timestamp_filters = extract_timestamp_filters_from_filters(filters)
        tickets = {}
        for key, ticket in self.db.items():
            if self._is_ticket_filtered(text_filters, timestamp_filters, ticket):
                tickets[key] = ticket
        return tickets

    @staticmethod
    def _is_ticket_filtered(text_filters, timestamp_filters, ticket):
        is_text_filter = is_text_filtered(text_filters, ticket) if text_filters else True
        is_timestamp_filter = is_timestamp_filtered(timestamp_filters, ticket) if timestamp_filters else True
        return is_text_filter and is_timestamp_filter
