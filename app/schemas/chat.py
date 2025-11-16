from pydantic import BaseModel

class ChatMessageCreate(BaseModel):
    username: str
    message: str
