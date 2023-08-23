from dataclasses import dataclass, field


@dataclass
class User:
    user_id: str
    username: str
    email: str
    password: str
    posts: list = field(default_factory=list)
