class UserNotExist(Exception):
    def __str__(self, user_id):
        return f"User id: {user_id} not exist"
