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


class UserFollowers(BaseModel):
    followers: List[str] = []
    followers_requested: List[str] = []

class UserFollowing(BaseModel):
    following: List[str] = []
    following_requested: List[str] = []

class UserProfileSchema(BaseModel):
    username: str
    email: EmailStr
    followers: UserFollowers
    following: UserFollowing
    posts: List[ProfilePostSchema] = []
    businesses_followed: List[str] = []

class UserSearchResponse(BaseModel):
    username: str
    email: EmailStr
