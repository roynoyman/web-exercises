import random
from dataclasses import asdict
from unittest import TestCase

from requests import HTTPError

from manage_users.api import app
from manage_users.helpers import generate_random_string
from manage_users.user import User


def create_random_user(username=None, email=None, password=None):
    username = username or generate_random_string()
    email = email or generate_random_string()
    password = password or generate_random_string()
    user = {'username': username, 'email': email, 'password': password}
    return user


class TestManageUsersApi(TestCase):
    url = "http://127.0.0.1:5000/users"

    def setUp(self) -> None:
        self.client = app.test_client()

    def tearDown(self) -> None:
        self.client.delete(self.url)

    def test_create_user(self):
        new_user = create_random_user()
        resp = self.client.post(self.url, json={"user": new_user})
        self.assertEqual(resp.status_code, 201)

    def test_create_user_missing_args(self):
        new_user = create_random_user()
        new_user.pop('username')

        resp = self.client.post(self.url, json={"user": new_user})
        self.assertEqual(resp.status_code, 400)
        self.assertIn('Missing required args for creating a user', resp.text)

    def test_get_user_not_exist(self):
        resp = self.client.get(f'{self.url}/some-not-exist-id')
        self.assertEqual(resp.status_code, 404)

    def test_get_user(self):
        users = self.insert_users_to_db(n=3)
        for user in users:
            self.client.post(self.url, json={"user": user})

        actual = self.client.get(f'{self.url}/1')
        actual_user = actual.json
        self.assertEqual(actual.status_code, 200)
        self.assertEqual(actual_user['email'], users[0].get('email'))

    def insert_users_to_db(self, n: int = 1) -> list[User]:
        new_users = []
        for i in range(n):
            new_users.append(create_random_user())
        return new_users
