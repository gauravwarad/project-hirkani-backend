import uuid
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List



class DiscoverListViewObject(BaseModel):
    business_name: str
    business_address: str
    business_rating: float
    business_id: str
    ratings: int
