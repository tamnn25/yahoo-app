from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str

class FriendRequest(BaseModel):
    username: str  # friend username
