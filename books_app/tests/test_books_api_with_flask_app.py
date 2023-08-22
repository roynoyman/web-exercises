import logging
from dataclasses import asdict
from unittest import TestCase

from books import create_new_book
from books_api import app

logger = logging.getLogger(__name__)


class TestBooksApi(TestCase):
    url = "http://127.0.0.1:5000/books"

    def setUp(self) -> None:
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.client.delete(self.url)

    def test_get_book_by_id(self):
        new_book = create_new_book()
        self.client.post(self.url, json={"book": asdict(new_book)})
        url = f'{self.url}/{new_book.book_id}'
        resp = self.client.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(asdict(new_book), resp.json)

    def test_post_new_book(self):
        new_book = create_new_book()
        resp = self.client.post(self.url, json={"book": asdict(new_book)})
        self.assertIn("Post book success", resp.text)

    def test_get_book_by_id_item_not_exist(self):
        book_id = "some-book-id"
        url = f'{self.url}/{book_id}'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)
        self.assertIn('Item not exist in DB', resp.text)

    def test_get_all_books_empty(self):
        actual = self.client.get(self.url)
        self.assertEqual([], actual.json)

    def test_get_all_books(self):
        book1 = create_new_book()
        book2 = create_new_book()
        expected = [book1, book2]
        self.insert_books(expected)
        resp = self.client.get(self.url)
        actual_books = resp.json
        self.assertIn(asdict(book1), actual_books)
        self.assertIn(asdict(book2), actual_books)
        self.assertEqual(2, len(actual_books))

    def test_update_book_correct_field(self):
        book_to_update = create_new_book()
        self.insert_books([book_to_update])
        expected_title_update = {"title": "some-title"}
        url = f'{self.url}/{book_to_update.book_id}'
        self.client.put(url, json=expected_title_update)

        actual_updated_book = self.client.get(url).json
        self.assertEqual(actual_updated_book.get("title"), expected_title_update.get('title'))

    def test_update_book_not_exist_book(self):
        not_exist_book_id = "not-exist"
        title_update = {"title": "some-title"}
        url = f'{self.url}/{not_exist_book_id}'
        resp = self.client.put(url, json=title_update)
        self.assertEqual(resp.status_code, 404)
        self.assertIn("Item not exist in DB", resp.text)

    def test_delete_book_by_id(self):
        book_to_delete = create_new_book()
        self.insert_books([book_to_delete])
        url = f'{self.url}/{book_to_delete.book_id}'
        actual_deleted = self.client.delete(url).json
        self.assertEqual(actual_deleted, asdict(book_to_delete))

    def test_delete_not_exist_book(self):
        book_to_delete = create_new_book()
        url = f'{self.url}/{book_to_delete.book_id}'
        actual_deleted_status_code = self.client.delete(url).status_code
        self.assertEqual(actual_deleted_status_code, 404)

    def test_delete_all(self):
        book1 = create_new_book()
        book2 = create_new_book()
        self.insert_books([book1, book2])
        actual_status_code = self.client.delete(self.url).status_code
        self.assertEqual(actual_status_code, 204)

    def insert_books(self, books_list):
        url = f'{self.url}'
        for book in books_list:
            self.client.post(url, json={"book": asdict(book)})
