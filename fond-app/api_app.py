import logging
import os
import signal

from flask import Flask, jsonify, request
from pymongo.errors import DuplicateKeyError

from cashback import Cashback
from db_utils import insert_one_cb, list_cashbacks, list_cashbacks_with_filter, \
    get_event_history_with_filter, post_event, update_event
from event import Event
from validations import get_args_from_req, format_exception

app = Flask(__name__)


@app.route('/')
def welcome():
    return jsonify('Welcome'), 200


@app.route('/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({"success": True, "message": "Server is shutting down..."})


@app.route('/cashbacks/', methods=(["GET"]))
def get_cashback():
    try:
        all_cashbacks = list_cashbacks()
    except Exception as e:
        return f"error: {e}", 400
    return jsonify(f'{all_cashbacks}'), 200


@app.route('/cashbacks/', methods=(["POST"]))
def post_cashback():
    try:
        args = get_args_from_req()
        new_cashback = Cashback.from_request(args)
        insert_one_cb(new_cashback.asdict())
    except KeyError:
        return format_exception(f"msg: Missing crucial required args - _id , amount, state"), 400
    return jsonify("success"), 201


@app.route('/cashbacks/<cashback_id>', methods=(["GET"]))
def get_chasback_id(cashback_id):
    cashback_spec = list_cashbacks_with_filter({'_id': cashback_id})
    # list(cashbacks.find({'_id': cashback_id}))
    return jsonify(f" Good: {cashback_id} is: {cashback_spec}"), 200


@app.route('/event/', methods=(["POST"]))
def post_event_processor():
    try:
        args = get_args_from_req()
        event = Event.from_request(args)
        res = post_event(event)
    except TypeError as e:
        return f"error: {e}"
    except DuplicateKeyError as e:
        return f"id: {args['cashback_id']} is already exist. \n {e}", 400
    return jsonify(f"post: {res}"), 201


@app.route('/event/', methods=(["PUT"]))
def update_event_proc():
    try:
        args = get_args_from_req()
        event = Event.from_request(args)
        res = update_event(event)
    except KeyError as e:
        return f"error: {e}", 400
    return f"id: {res}", 201


@app.route('/event/<cashback_id>', methods=(["GET"]))
def get_events(cashback_id):
    try:
        logging.info(f"cashback id is: {cashback_id}")
        cashback_events = get_event_history_with_filter({'_id': cashback_id})
    except TypeError as e:
        return
    return jsonify(f"cashback id: {cashback_id} has {len(cashback_events)} events. \n {cashback_events}"), 200
