from fastapi_users import schemas
import uuid
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    username: str

class UserUpdate(schemas.BaseUserUpdate):
    pass

class ProfilePostSchema(BaseModel):
    id: int
    title: str
    content: str
    rating: float
    created_at: datetime

class UserProfileSchema(BaseModel):
    username: str
    email: EmailStr
    followers: List[str] = []
    following: List[str] = []
    posts: List[ProfilePostSchema] = []