import random
from dataclasses import dataclass, asdict
from typing import List

from helpers import generate_random_string


def validate_properties(key, value):
    if not key and not value:
        raise KeyError


@dataclass
class Book:
    book_id: str
    title: str
    author: str
    publication_year: int

    def from_req_args(self, **kwargs):
        return Book(**kwargs)

    def __eq__(self, other):
        return self.book_id == other.book_id

    def __gt__(self, other):
        return self.book_id > other.book_id

    def __setattr__(self, key, value):
        validate_properties(key, value)
        super().__setattr__(key, value)


def create_new_book(book_id=None, title=None, author=None, publication_year=None):
    book_id = book_id or generate_random_string()
    title = title or generate_random_string()
    author = author or generate_random_string()
    publication_year = publication_year or random.randint(0, 2023)

    return Book(book_id, title, author, publication_year)


def create_many_bew_books(amount: int, book_id=None, title=None, author=None, publication_year=None) -> List:
    books_list = []
    for i in range(amount):
        books_list.append(create_new_book(book_id, title, author, publication_year))
