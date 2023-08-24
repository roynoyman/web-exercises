import os
import signal

from flask import Flask, jsonify, Request

from manage_users.database import UsersDBDict
from manage_users.exceptions import UserNotExist
from manage_users.helpers import get_args_from_req
from manage_users.user import User

app = Flask(__name__)
database = UsersDBDict()


@app.route('/')
def welcome():
    return jsonify('Welcome'), 200


@app.route('/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({"success": True, "message": "Server is shutting down..."})


# Get book by id
@app.route('/users/<user_id>', methods=(["GET"]))
def get_user_by_id(user_id):
    try:
        user = database.get_user(user_id=user_id)
    except UserNotExist as e:
        return f"error: user id: {user_id} not exist", 404
    except Exception as e:
        return f"error: {e}", 500
    return jsonify(user), 200


# # Get All Books
# @app.route('/books', methods=(["GET"]))
# def get_books():
#     try:
#         books = database.get_all()
#     except Exception as e:
#         return f"error: {e}", 400
#     return jsonify(books), 200


@app.route('/users', methods=(["POST"]))
def create_user():
    try:
        args = get_args_from_req()
        # validate_book_args(args)
        new_user = User(**args)
        database.create_user(key=new_user.user_id, value=new_user)
    except TypeError:
        return jsonify(f"msg: Missing required args for creating a user"), 400
    except Exception as e:
        return jsonify(e), 500
    return jsonify(new_user.user_id), 201


# @app.route('/books/<book_id>', methods=(["PUT"]))
# def update_book_by_id(book_id):
#     try:
#         args = get_args_from_req()
#         validate_book_args(args)
#         database.update_one(book_id, args)
#     except ItemNotExist as e:
#         return f"error: {e}", 404
#     except KeyError as e:
#         return f"error: key doesn't exist: {e}", 400
#     return jsonify(f'{book_id} was updated'), 200
#
#
# @app.route('/books/<book_id>', methods=(["DELETE"]))
# def delete_book_by_id(book_id):
#     try:
#         book = database.delete_one(book_id)
#     except ItemNotExist as e:
#         return f"error: {e}", 404
#     return jsonify(book), 200
#
#
@app.route('/users', methods=(["DELETE"]))
def delete_all_users():
    try:
        database.delete_all()
    except Exception as e:
        return f"Server error: {e}", 500
    return jsonify(), 204
