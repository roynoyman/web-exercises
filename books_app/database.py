from books import Book
from exceptions import ItemNotExist


class DataBase:
    def get_one(self, book_id: str) -> dict:
        pass

    def get_all(self) -> list[Book]:
        pass

    def insert_one(self, book: Book) -> None:
        pass

    def update_one(self, book_id, key_value_update_fields: dict):
        pass

    def delete_one(self, book_id) -> Book:
        pass


class DictDataBase(DataBase):
    database: dict

    def __init__(self):
        self.database = dict()

    def get_one(self, book_id: str) -> Book:
        book = self.database.get(book_id)
        if not book:
            raise ItemNotExist
        return book

    def get_all(self) -> list:
        return list(self.database.values())

    def insert_one(self, book: Book) -> None:
        print(f"{book.book_id}: book.book_id")
        self.database[book.book_id] = book

    def update_one(self, book_id, key_value_update_fields: dict):
        exist_book = self.database.get(book_id)
        if not exist_book:
            raise ItemNotExist()
        if exist_book:
            for k in key_value_update_fields:
                setattr(exist_book, k, key_value_update_fields[k])

    def delete_one(self, book_id):
        try:
            removed_book = self.database.pop(book_id)
        except KeyError():
            raise ItemNotExist()
        return removed_book

    def check_id_in_db(self, book_id):
        return True if book_id in self.database else False

    def delete_all(self):
        self.database = dict()
