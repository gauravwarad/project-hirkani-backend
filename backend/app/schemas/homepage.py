from fastapi_users import schemas
import uuid
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List


class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    rating: float
    created_at: datetime
    username: str
    likes: int = 0
    is_liked: bool = False

class HomePagePostRequest(BaseModel):
    skip: int = 0
    limit: int = 10