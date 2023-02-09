import json
import unittest

import requests
from cashback import Cashback


class TestFondApp(unittest.TestCase):
    def test_cashback_from_req_missing_amount_param(self):
        cb_dict = {"cb_id": 'goodId',
                   "merchant_name": "Nike",
                   "customer_name": "goodName",
                   "customer_email": "goodUser@gmail.com",
                   "created_at": "good date"}
        with self.assertRaises(TypeError) as e:
            Cashback(cb_dict)

    def test_cashback_failure_bad_id(self):
        cb_dict = {"cashback_id": 'badId',
                   "amount": "10000",
                   "merchant_name": "Nike",
                   "customer_name": "goodName",
                   "customer_email": "goodUser@gmail.com"}
        url = f'http://127.0.0.1:5000/cashback'
        resp = requests.post(url, params=cb_dict)
        self.assertEqual(403, resp.status_code)

    def test_cashback_success_(self):
        cb_dict = {"cashback_id": 'goodId',
                   "amount": "10000",
                   "merchant_name": "Nike",
                   "customer_name": "goodName",
                   "customer_email": "goodUser@gmail.com"}
        url = f'http://127.0.0.1:5000/cashback/'
        resp = requests.post(url, params=cb_dict)
        self.assertEqual(200, resp.status_code)

    def test_reserve_balance_success(self):
        cb_dict = {"cb_id": 'goodId',
                   "amount": "100000",
                   "merchant_name": "Nike",
                   "customer_name": "goodName",
                   "customer_email": "goodUser@gmail.com",
                   "created_at": "good date"}
        url = f'http://rollback.proxy.beeceptor.com/reserve_balance/{cb_dict["cb_id"]}'
        # Additional headers.
        headers = {'Content-Type': 'application/json'}
        resp = requests.post(url, headers=headers)
        self.assertEqual(200, resp.status_code)

    def test_reserve_balance_no_balance(self):
        cb_dict = {"cb_id": 'badId',
                   "amount": "100000",
                   "merchant_name": "Nike",
                   "customer_name": "goodName",
                   "customer_email": "goodUser@gmail.com",
                   "created_at": "good date"}
        url = f'http://rollback.proxy.beeceptor.com/reserve_balance/{cb_dict["cb_id"]}'
        # Additional headers.
        headers = {'Content-Type': 'application/json'}
        resp = requests.post(url, headers=headers)
        self.assertEqual(403, resp.status_code)

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
