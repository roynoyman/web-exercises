from manage_users.exceptions import UserNotExist
from manage_users.user import User


class ManageUsersDB:
    def get_user(self, user_id: str) -> User:
        pass

    def create_user(self, user: User) -> None:
        pass

    def delete_all(self) -> None:
        pass


class UsersDBDict(ManageUsersDB):
    db = dict()

    def get_user(self, user_id: str) -> User:
        user = self.db.get(user_id)
        if not user:
            raise UserNotExist(user_id)
        return user

    def create_user(self, key: str, value: User) -> None:
        self.db[key] = value

    def delete_all(self) -> None:
        self.db = dict()
