import time
import unittest
from dataclasses import asdict
from pathlib import Path

from database.database import SimpleTicketsDictDataBase
from api.exceptions import NotSupportedFilters
from api.helpers import validate_filter_keys
from data.pre_load_data import read_data_from_file, pre_load_tickets, insert_tickets_to_db
from database.ticket import Ticket
from database.db_helpers import extract_timestamp_filters_from_filters, extract_text_filters_from_filters


class TestPreLoadDataToDB(unittest.TestCase):
    test_data_json_path = f'{Path(__file__).parent.parent}/data/data_for_tests.json'

    def test_read_data_from_file(self):
        expected_ticket_id_1 = "1"
        expected_user_email_2 = "user2@example.com"

        tickets_data = read_data_from_file(self.test_data_json_path)

        self.assertEqual(tickets_data[0]["id"], expected_ticket_id_1)
        self.assertEqual(tickets_data[1]["userEmail"], expected_user_email_2)
        self.assertEqual(len(tickets_data), 2)

    def test_pre_load_tickets_e2e(self):
        expected_ticket_id_1 = "1"
        expected_user_email_2 = "user2@example.com"

        test_db = SimpleTicketsDictDataBase()
        pre_load_tickets(self.test_data_json_path, test_db)

        self.assertIn(expected_ticket_id_1, test_db.db)
        self.assertEqual(test_db.db['2'].userEmail, expected_user_email_2)
        self.assertEqual(len(test_db.db), 2)

    def test_insert_tickets_to_db(self):
        ticket = Ticket(id='some-id', title='some-title', content='some-content',
                        userEmail='some-email@wix.com', creationTime=time.time(),
                        labels=["some-labels"])
        tickets_data_to_insert = [asdict(ticket)]
        test_db = SimpleTicketsDictDataBase()
        insert_tickets_to_db(tickets_data_to_insert, test_db)

        self.assertIn(ticket.id, test_db.db)
        self.assertEqual(len(test_db.db), 1)


class TestHelperFunctions(unittest.TestCase):

    def test_validate_supported_filter_keys(self):
        success_filters = ['title', 'content', 'userEmail', 'from', 'to']

        validation_result = validate_filter_keys(success_filters)
        self.assertEqual(validation_result, True)

    def test_validate_unsupported_filter_keys(self):
        not_allowed_filters = ['not-allowed-filter']

        with self.assertRaises(NotSupportedFilters):
            validation_result = validate_filter_keys(not_allowed_filters)


class TestDBHelperFunctions(unittest.TestCase):
    def test_extract_text_filters(self):
        expected_text_filters = {'title': 'some-title', 'content': 'some-id', 'userEmail': "some-email@wix.com"}

        actual_text_filters = extract_text_filters_from_filters(expected_text_filters)
        self.assertEqual(actual_text_filters, expected_text_filters)

    def test_extract_text_filters_with_unsupported_filters(self):
        unsupported_text_filters = {'not-supported-filter-1': 'some-title', 'not-supported-filter2': 'some-id'}

        actual_text_filters = extract_text_filters_from_filters(unsupported_text_filters)
        self.assertEqual(actual_text_filters, None)

    def test_extract_timestamp_filters(self):
        expected_timestamp_filters = {'from': 100, 'to': time.time()}

        actual_timestamp_filters = extract_timestamp_filters_from_filters(expected_timestamp_filters)
        self.assertEqual(actual_timestamp_filters, expected_timestamp_filters)

    def test_extract_timestamp_filters_no_from_filter(self):
        timestamp_filters = {'to': time.time()}
        expected_timestamp_filters = {**timestamp_filters, 'from': 0}

        actual_timestamp_filters = extract_timestamp_filters_from_filters(timestamp_filters)
        self.assertEqual(actual_timestamp_filters, expected_timestamp_filters)

    def test_extract_timestamp_filters_no_to_filter(self):
        timestamp_filters = {'from': 1500}
        # expected_timestamp_filters = {**timestamp_filters, 'to': time.time()}

        actual_timestamp_filters = extract_timestamp_filters_from_filters(timestamp_filters)
        self.assertIn('to', actual_timestamp_filters.keys())

    def test_extract_timestamp_filters_with_unsupported_filters(self):
        unsupported_timestamp_filters = {'not-supported-filter-1': 'some-timestamp-value', 'not-supported-filter2': 1000}

        actual_text_filters = extract_text_filters_from_filters(unsupported_timestamp_filters)
        self.assertEqual(actual_text_filters, None)
