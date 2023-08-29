import logging
from dataclasses import asdict
from unittest import TestCase

from requests import HTTPError

from books import create_new_book
from lib.books_client import BooksClient
from tests.web_server_tests import WebServerBooks

logger = logging.getLogger(__name__)


class TestBooksApi(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = WebServerBooks().start()
        cls.client = BooksClient(url=cls.server.url)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def tearDown(self) -> None:
        self.server.reset_database()

    def test_get_book_by_id(self):
        book_id = "some-book-id"
        new_book = create_new_book(book_id=book_id)
        self.server.database.insert_one(new_book)

        actual = self.client.get_book_by_id(book_id)
        self.assertEqual(actual, asdict(new_book))

    def test_post_new_book(self):
        new_book = create_new_book()
        resp = self.client.post_book(new_book)
        self.assertIn("Post book success", resp)
        self.assertTrue(new_book.book_id, self.server.database.check_id_in_db(new_book.book_id))

    def test_get_book_by_id_item_not_exist(self):
        book_id = "some-book-id"
        with self.assertRaisesRegex(HTTPError, "NOT FOUND for url"):
            self.client.get_book_by_id(book_id)

    def test_get_all_books_empty(self):
        actual = self.client.get_books()
        self.assertEqual([], actual)

    def test_get_all_books(self):
        book1 = create_new_book()
        book2 = create_new_book()
        expected = [book1, book2]
        self.insert_books(expected)

        actual = self.client.get_books()
        self.assertIn(asdict(book1), actual)
        self.assertIn(asdict(book2), actual)
        self.assertEqual(2, len(actual))

    def test_post_new_book(self):
        new_book = create_new_book()
        resp = self.client.post_book(new_book)
        self.assertIn("Post book success", resp)
        self.assertTrue(new_book.book_id, self.server.database.check_id_in_db(new_book.book_id))

    def test_update_book_correct_field(self):
        book_to_update = create_new_book()
        self.insert_books([book_to_update])
        expected_title = {"title": "some-title"}
        self.client.update_book(book_to_update.book_id, expected_title)

        actual_update_book = self.server.database.get_one(book_to_update.book_id)
        self.assertEqual(actual_update_book.title, actual_update_book.title)

    def test_delete_book_by_id(self):
        book_to_delete = create_new_book()
        self.server.database.insert_one(book_to_delete)
        # Sanity check:
        self.assertEqual(True, self.server.database.check_id_in_db(book_to_delete.book_id))

        self.client.delete_book(book_to_delete.book_id)
        self.assertEqual(False, self.server.database.check_id_in_db(book_to_delete.book_id))

    def insert_books(self, books_list):
        for book in books_list:
            self.server.database.insert_one(book)
