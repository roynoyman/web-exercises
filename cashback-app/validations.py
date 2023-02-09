import requests
from flask import jsonify, request

from cashback import Cashback


def get_args_from_req():
    return request.args


def validate_screen(name):
    url = f'http://rollback.proxy.beeceptor.com/screen/{name}'
    # Additional headers.
    headers = {'Content-Type': 'application/json'}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 403:
        raise ValueError("bad name - screening fail")
    return


def validate_cb_id_already_exist(cb_id):
    # CHECK IN DB IF ID ALREADY EXIST
    return


def validate_balance(new_cashback: Cashback):
    url = f'http://rollback.proxy.beeceptor.com/reserve_balance/{new_cashback._id}'
    # Additional headers.
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(url, headers=headers, data=(
        {"id": new_cashback._id, "amount": new_cashback.amount, "customer_email": new_cashback.customer_email}))
    if resp.status_code == 403:
        raise ValueError(f"bad reserve_balance - fail, \n {resp.text}")


def release_balance(cb_id: str):
    url = f'http://rollback.proxy.beeceptor.com/reserve_balance/{cb_id}'
    # Additional headers.
    headers = {'Content-Type': 'application/json'}
    resp = requests.delete(url)
    return "released. reserved balanced was deleted"
