import os
import signal

from flask import Flask, jsonify, Request

from books import Book
from database import DictDataBase
from exceptions import ItemNotExist, format_exception
from helpers import get_args_from_req
from validations import validate_book_args

app = Flask(__name__)
database = DictDataBase()


@app.route('/')
def welcome():
    return jsonify('Welcome'), 200


@app.route('/stopServer', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({"success": True, "message": "Server is shutting down..."})


# Get book by id
@app.route('/books/<book_id>', methods=(["GET"]))
def get_book_by_id(book_id):
    try:
        book = database.get_one(book_id)
    except ItemNotExist as e:
        return format_exception(e), 404
    except Exception as e:
        return f"error: {e}", 500
    return jsonify(book), 200


# Get All Books
@app.route('/books', methods=(["GET"]))
def get_books():
    try:
        books = database.get_all()
    except Exception as e:
        return f"error: {e}", 400
    return jsonify(books), 200


@app.route('/books', methods=(["POST"]))
def post_book():
    try:
        args = get_args_from_req()
        validate_book_args(args)
        book_dict = args["book"]
        new_book = Book(**book_dict)
        database.insert_one(new_book)
    except Exception as e:
        return jsonify(e), e.status_code
    except KeyError:
        return jsonify(f"msg: Missing crucial required args - _id , amount, state"), 400
    return jsonify(f"Post book success: {new_book.book_id}"), 201


@app.route('/books/<book_id>', methods=(["PUT"]))
def update_book_by_id(book_id):
    try:
        args = get_args_from_req()
        validate_book_args(args)
        print("args are:", args)
        database.update_one(book_id, args)
    except ItemNotExist as e:
        return f"error: {e}", 404
    except KeyError as e:
        return f"error: key doesn't exist: {e}", 400
    return jsonify(f'{book_id} was updated'), 200


@app.route('/books/<book_id>', methods=(["DELETE"]))
def delete_book_by_id(book_id):
    try:
        book = database.delete_one(book_id)
    except ItemNotExist as e:
        return f"error: {e}", 404
    return jsonify(book), 200


@app.route('/books', methods=(["DELETE"]))
def delete_all_books():
    try:
        database.delete_all()
    except Exception as e:
        return f"Server error: {e}", 500
    return jsonify(), 204
