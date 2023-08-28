import unittest
from pathlib import Path

from api import app
from pre_load_data import read_data_from_file

actual_data_path = f'{Path(__file__).parent.parent}/data.json'


def expected_tickets_helper():
    tickets_list = read_data_from_file(actual_data_path)
    return {ticket["id"]: ticket for ticket in tickets_list}


class TestTickets(unittest.TestCase):
    url = "http://127.0.0.1:5000/tickets"

    def setUp(self) -> None:
        self.client = app.test_client()

    def test_get_tickets_no_filters(self):
        expected_tickets = expected_tickets_helper()

        resp = self.client.get(self.url)
        actual_tickets = resp.json

        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected_tickets, actual_tickets)

    def test_get_tickets_with_filter(self):
        expected_tickets = expected_tickets_helper()
        expected_ticket_id = '1'
        expected_ticket_tile = expected_tickets.get(expected_ticket_id).get("title")

        resp = self.client.get(self.url, json={'title': expected_ticket_tile})
        actual_tickets = resp.json

        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected_tickets.get(expected_ticket_id), actual_tickets.get(expected_ticket_id))
        self.assertEqual(len(actual_tickets), 1)

    def test_get_tickets_with_title_and_content_filters(self):
        expected_tickets = expected_tickets_helper()
        expected_ticket_id = '3'
        expected_ticket_tile = expected_tickets.get(expected_ticket_id).get("title")
        expected_ticket_content = expected_tickets.get(expected_ticket_id).get("content")

        resp = self.client.get(self.url, json={'title': expected_ticket_tile, 'content': expected_ticket_content})
        actual_tickets = resp.json

        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected_tickets.get(expected_ticket_id), actual_tickets.get(expected_ticket_id))
        self.assertEqual(expected_tickets.get('4'), actual_tickets.get('4'))
        self.assertEqual(len(actual_tickets), 2)
