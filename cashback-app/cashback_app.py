import logging
import os
import signal

from flask import Flask, jsonify, request
from pymongo.errors import DuplicateKeyError

from cashback import Cashback
from db_utils import insert_cashback_to_db
from validations import get_args_from_req, validate_screen, validate_balance, validate_cb_id_already_exist, \
    release_balance

app = Flask(__name__)


@app.route('/')
def welcome():
    return jsonify('Welcome'), 200


@app.route('/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({"success": True, "message": "Server is shutting down..."})


@app.route('/cashback/', methods=(["POST"]))
def post_cashback():
    try:
        args = get_args_from_req()
        new_cashback = Cashback.from_request(args)
    except TypeError as e:
        return jsonify(f"missing args, follow api guidelines \n {e}"), 400
    except Exception as e:
        return jsonify(f"{e}"), 405
    try:
        validate_balance(new_cashback)
    except ValueError as e:
        return jsonify(f"Reserve balance failed \n {e}"), 403
    try:
        validate_cb_id_already_exist(new_cashback._id)
        validate_screen(new_cashback.customer_name)
        insert_cashback_to_db(new_cashback.asdict())
    except ValueError as e:
        released = release_balance(new_cashback._id)
        return jsonify(f"{e}, balance released={released}"), 403
    send_email_on_success(new_cashback._id)
    return jsonify(f"cashback posted, id: {new_cashback._id}"), 200
