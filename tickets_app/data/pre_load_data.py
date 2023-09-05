import json

from database.database import TicketsDataBase
from database.ticket import Ticket


def insert_tickets_to_db(tickets_data, database: TicketsDataBase):
    for ticket_data in tickets_data:
        ticket = Ticket(**ticket_data)
        database.insert_ticket(ticket.id, ticket)


def read_data_from_file(file_path):
    with open(file_path) as tickets_file:
        tickets_data = json.load(tickets_file)
    return tickets_data


def pre_load_tickets(data_path, database):
    tickets_data = read_data_from_file(data_path)
    insert_tickets_to_db(tickets_data, database)
