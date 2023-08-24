from dataclasses import dataclass, field

users = 0


class UsersAll:
    users = 0

    @classmethod
    def create_user_id(cls):
        cls.users = cls.users + 1
        return cls.users


# def create_user_id():
#     new_user_id = users
#     users = users + 1
#     return new_user_id


@dataclass
class User:
    user_id: str
    username: str
    email: str
    password: str
    posts: list

    def __init__(self, username, email, password):
        self.user_id = f'{UsersAll.create_user_id()}'
        self.username = username
        self.email = email
        self.password = password
        self.posts = list()
