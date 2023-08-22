from dataclasses import asdict

from requests import get, post, delete, put, Response
from requests.exceptions import ConnectionError, Timeout, HTTPError
from retry import retry
from wix_legacy_logger.logger import WixLogger

from exceptions import ItemNotExist


class RetryableHTTPError(HTTPError):
    pass


retryable_exceptions = (Timeout, ConnectionError, RetryableHTTPError)


class BooksClient:
    def __init__(self, url):
        self.url = url
        self.logger = WixLogger(__name__, level=WixLogger.INFO)

    def get_book_by_id(self, book_id):
        return self._get(f'books/{book_id}')

    def get_books(self) -> list:
        return self._get('books')

    def post_book(self, book: dict):
        return self._post('books', json={"book": asdict(book)})

    def update_book(self, book_id: str, books_fields_update: dict):
        return self._put(f'books/{book_id}', json=books_fields_update)

    def delete_book(self, book_id: str):
        return self._delete(f'books/{book_id}')

    def delete_all_books(self):
        return self._delete(f'books')

    @retry(exceptions=retryable_exceptions, tries=3, delay=0.1)
    def _get(self, path, params=None, timeout=(1, 10), **kwargs):
        response = get(f'{self.url}/{path}', params=params, timeout=timeout, **kwargs)
        return self._handle_response(response, self.logger)

    @retry(exceptions=retryable_exceptions, tries=3, delay=0.1)
    def _post(self, path, data=None, json=None, timeout=200, **kwargs):
        response = post(f'{self.url}/{path}', data=data, json=json, timeout=timeout, **kwargs)
        return self._handle_response(response, self.logger)

    @retry(exceptions=retryable_exceptions, tries=3, delay=0.1)
    def _put(self, path, data=None, json=None, timeout=200, **kwargs):
        response = put(f'{self.url}/{path}', data=data, json=json, timeout=timeout, **kwargs)
        return self._handle_response(response, self.logger)

    @retry(exceptions=retryable_exceptions, tries=3, delay=0.1)
    def _delete(self, path, data=None, json=None, timeout=200, **kwargs):
        response = delete(f'{self.url}/{path}', data=data, json=json, timeout=timeout, **kwargs)
        return self._handle_response(response, self.logger)

    @staticmethod
    def _handle_response(response: Response, logger: WixLogger):
        try:
            response.raise_for_status()
        except HTTPError as e:
            if 500 <= e.response.status_code <= 600:
                raise RetryableHTTPError(f'Server error with code :{e.response.status_code} reason:{e.response.reason}',
                                         response=e.response)
            else:
                logger.error(f"Request failed. Wix Request ID: {response.headers.get('X-Wix-Request-Id')}")
                logger.error(f"Request full headers: {response.headers}")
                raise e

        return response.json()
