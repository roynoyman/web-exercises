import unittest

from manage_users.post import Post
from manage_users.user import User


class TestDataClasses(unittest.TestCase):
    def test_user_creation(self):
        expected_user_id = "some-id"
        expected_username = 'some-username'
        expected_email = "some-email@wix.com"
        expected_password = '12345'
        user = User(user_id=expected_user_id, username=expected_username, email=expected_email,
                    password=expected_password)
        self.assertEqual(user.user_id, expected_user_id)
        self.assertEqual(user.posts, [])
        self.assertEqual(user.email, expected_email)

    def test_post_creation(self):
        expected_title = "some-title"
        expected_user_id = 'some-username'
        expected_content = "content"
        post = Post(title=expected_title, user_id=expected_user_id, content=expected_content)
        self.assertEqual(post.user_id, expected_user_id)
        self.assertEqual(post.content, expected_content)
        self.assertEqual(post.title, expected_title)
