from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List



class GetProfilePostSchema(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

class GetUserProfileSchema(BaseModel):
    username: str
    following: bool # either "following", "requested", or "follow"
    posts: List[GetProfilePostSchema] = []

class Message(BaseModel):
    message: str