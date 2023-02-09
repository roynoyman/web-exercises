import json
import unittest

import requests

from event import Event


class TestFondApp(unittest.TestCase):
    def test_event_from_req_missing_type(self):
        event_id = '1'
        with self.assertRaises(TypeError) as e:
            Event({'cashback_id': event_id})

    def test_event_from_req_missing_id(self):
        type = 'created'
        with self.assertRaises(TypeError) as e:
            Event({'type': type})

    def test_event_created(self):
        id = "1"
        e_type = 'create'
        event = Event.from_request({"cashback_id": id, "type": e_type})
        self.assertIsInstance(event, Event)

    def test_get_cashbacks(self):
        url = 'http://127.0.0.1:5000/cashbacks'
        # Additional headers.
        headers = {'Content-Type': 'application/json'}
        resp = requests.get(url, headers=headers)
        self.assertEqual(200, resp.status_code)

    def test_post_cashback(self):
        url = 'http://127.0.0.1:5000/cashbacks'
        # Additional headers.
        headers = {'Content-Type': 'application/json'}
        cb = {'_id': 10,
              'amount': 100,
              'state': "created",
              'valid': "valid"}
        resp = requests.post(url, headers=headers, params=cb)
        self.assertEqual(201, resp.status_code)
