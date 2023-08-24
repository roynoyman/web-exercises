import unittest
from pathlib import Path

from pre_load_data import read_data_from_file


class TestHelperFunctions(unittest.TestCase):
    def test_pre_load_data_to_db(self):
        expected_ticket_id_1 = "1"
        expected_user_email_2 = "user2@example.com"

        data_json_path = f'{Path(__file__).parent}/data_for_tests.json'
        tickets_data = read_data_from_file(data_json_path)

        self.assertEqual(tickets_data[0]["id"], expected_ticket_id_1)
        self.assertEqual(tickets_data[1]["userEmail"], expected_user_email_2)
        self.assertEqual(len(tickets_data), 2)
