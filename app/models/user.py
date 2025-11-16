from dataclasses import dataclass

@dataclass
class User:
    def __init__(self, id: int, username: str, password: str, token: str = None):
        self.id = id
        self.username = username
        self.password = password
        self.token = token


@dataclass
class Friend:
    user_id: int
    friend_id: int