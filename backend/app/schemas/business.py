import uuid
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List


class BusinessPosts(BaseModel):
    id: int
    title: str
    content: str
    posted_at: datetime = None

class GetBusinessProfileObject(BaseModel):
    # name, address, followers count, posts, average rating among your friends
    name: str
    address: str
    followers_count: int
    posts: List[BusinessPosts]
    average_rating: float
    num_ratings: int
    is_followed: bool = False
    is_handler: bool = False

class BusinessHandlerCheck(BaseModel):
    business_id: str
    answer: bool

class ClaimBusiness(BaseModel):
    google_id: str # google place id
    name: str
    address: str

class NewBusinessPost(BaseModel):
    title: str
    content: str
    business_id: str
