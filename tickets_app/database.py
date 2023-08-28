from ticket import Ticket


class TicketsDataBase:
    def get_ticket_by_id(self, ticket_id):
        pass

    def get_all_tickets(self, filter_params=None) -> dict[str:Ticket]:
        pass

    def insert_ticket(self, ticket_id, ticket) -> None:
        pass


class SimpleTicketsDictDataBase(TicketsDataBase):
    db = dict()

    def get_ticket_by_id(self, ticket_id):
        return self.db.get(ticket_id)

    def get_all_tickets(self, filters=None) -> dict[str:Ticket]:
        if not filters:
            return self.db
        return self._get_tickets_with_filters(filters)

    def insert_ticket(self, ticket_id, ticket):
        self.db[ticket_id] = ticket

    def _get_tickets_with_filters(self, filters):
        tickets = {}
        for key, ticket in self.db.items():
            if all(getattr(ticket, field) == value for field, value in filters.get('text_filters').items()):
                tickets[key] = ticket
        return tickets
