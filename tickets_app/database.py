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

    def get_all_tickets(self, filter_params=None) -> dict[str:Ticket]:
        if filter_params:
            return self._get_tickets_with_filters(filter_params)
        return self.db

    def insert_ticket(self, ticket_id, ticket):
        self.db[ticket_id] = ticket

    def _get_tickets_with_filters(self, filter_params):
        tickets = {}
        for key, ticket in self.db:
            for param, param_value in filter_params:
                if ticket.get(param) != param_value:
                    break
