import unittest

import requests

from cashback import Cashback


class TestFondApp(unittest.TestCase):
    # Didnt have time to add setup and teardown classes so tests wont imact each other and db will be clean.
    # Some tests are missing - reserve, screen etc.
    def test_cashback_from_req_missing_amount_param(self):
        cb_dict = {"cb_id": 'goodId',
                   "merchant_name": "Nike",
                   "customer_name": "goodName",
                   "customer_email": "goodUser@gmail.com",
                   }
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
        resp = requests.post(url, headers=headers, data=(
            {"id": cb_dict['cb_id'], "amount": cb_dict['amount'], "customer_email": cb_dict['customer_email']}))
        self.assertEqual(200, resp.status_code)

    def test_reserve_balance_fail(self):
        cb_dict = {"cb_id": 'badId',
                   "amount": "100000",
                   "merchant_name": "Nike",
                   "customer_name": "goodName",
                   "customer_email": "goodUser@gmail.com",
                   "created_at": "good date"}
        url = f'http://rollback.proxy.beeceptor.com/reserve_balance/{cb_dict["cb_id"]}'
        # Additional headers.
        headers = {'Content-Type': 'application/json'}
        resp = requests.post(url, headers=headers, data=(
            {"id": cb_dict['cb_id'], "amount": cb_dict['amount'], "customer_email": cb_dict['customer_email']}))
        self.assertEqual(403, resp.status_code)
