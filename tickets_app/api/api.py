import os
import signal
from pathlib import Path

from flask import Flask, jsonify

from database.database import SimpleTicketsDictDataBase
from api.exceptions import NotSupportedFilters
from api.helpers import get_filter_params_from_request
from data.pre_load_data import pre_load_tickets

app = Flask(__name__)
database = SimpleTicketsDictDataBase()
dir_path = Path(__file__).parent.parent
data_json_path = f'{dir_path}/data/data.json'

pre_load_tickets(data_json_path, database)


@app.route('/')
def welcome():
    return jsonify('Welcome'), 200


@app.route('/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({"success": True, "message": "Server is shutting down..."})


# Get ticket by id
@app.route('/tickets/<ticket_id>', methods=(["GET"]))
def get_ticket_by_id(ticket_id):
    try:
        ticket = database.get_ticket_by_id(ticket_id)
    # except ItemNotExist as e:
    #     return format_exception(e), 404
    except Exception as e:
        return f"error: {e}", 500
    return jsonify(ticket), 200


@app.route('/tickets', methods=(["GET"]))
def get_tickets_with_filters():
    try:
        filters = get_filter_params_from_request()
        tickets = database.get_all_tickets(filters)
    except NotSupportedFilters as e:
        return f"error: {e}", 400
    except Exception as e:
        return f"error: {e}", 500
    return jsonify(tickets), 200

