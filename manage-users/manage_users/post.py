from dataclasses import dataclass


@dataclass
class Post:
    title: str
    content: str
    user_id: str
