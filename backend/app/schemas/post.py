from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class SearchRequest(BaseModel):
    textQuery: str

class PlaceSearch(BaseModel):
    id: str
    name: str
    address: str

class PlacesSearchResult(BaseModel):
    places: List[PlaceSearch]

class CreatePost(BaseModel):
    business_id: str # which actually is the google place id
    title: str
    text: str
    rating: float
    