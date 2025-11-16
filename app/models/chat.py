from dataclasses import dataclass

@dataclass
class ChatMessage:
    id: int
    user_id: int
    username: str
    message: str
    timestamp: str
