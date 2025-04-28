import os
from fastapi import APIRouter, Depends, HTTPException, Query
import requests
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.post import CreatePost, PlaceSearch, PlacesSearchResult, SearchRequest
from app.models.user import User
from app.models.business import Business
from app.schemas.follow import Message
from app.models.post import Post
from ..dependencies import get_db
from app.auth import current_active_user

post_router = APIRouter(tags=["Post"])


@post_router.post("/post", response_model=Message)
async def add_post(request: CreatePost, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    # new post
    # posts table - id, poster (userid), title, text, timestamp
    # make a new entry in posts table.
    # look up  business_id in the business table to get the google place id
    # if not found, add a new entry in the business table and get the business id

    result = await db.execute(select(Business).filter(Business.google_id == request.business_id))
    business_exists = result.scalar_one_or_none()
    if business_exists:
        real_business_id = business_exists.id
    else:
        business = Business(google_id=request.business_id, name=request.business_name, address=request.business_address) 
        # handler id is null
        db.add(business)
        await db.commit()
        result = await db.execute(select(Business).filter(Business.google_id == request.business_id))
        real_business_id = result.scalar().id
        # uncomment and check if below works
        # await db.refresh(business)  
        # real_business_id = business.id
    post = Post(
        poster_id=user.id,
        title=request.title,
        text=request.text,
        rating=request.rating,
        business_id=real_business_id,
        likes=0,
    )
    db.add(post)
    await db.commit()
    return {"message": "Post created successfully"}


@post_router.post("/search_places",  response_model=PlacesSearchResult)
async def search_places(request: SearchRequest, user = Depends(current_active_user)):

    # Load API Key from environment variables
    GOOGLE_MAPS_API_KEY = os.getenv("API_KEY")
    GOOGLE_PLACES_URL = "https://places.googleapis.com/v1/places:searchText"
    
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.id"
    }
    
    payload = {"textQuery": request.textQuery}
    # print("i have the payload ", payload)
    # print("api key? ", GOOGLE_MAPS_API_KEY)
    # Make request to Google Places API
    response = requests.post(GOOGLE_PLACES_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching places")

    data = response.json()
    # Extract and return required fields
    results = [
        PlaceSearch(
            id=place.get("id", ""),
            name=place.get("displayName", {}).get("text", ""),
            address=place.get("formattedAddress", "")
        )
        for place in data.get("places", [])
    ]
    # print(data)
    return PlacesSearchResult(places=results)


# delete post api
# remove the post from posts table, remove the likes from likes table, keep the business entry in the business table
@post_router.delete("/delete-post/{post_id}", response_model=Message)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    # check if the post exists
    result = await db.execute(select(Post).filter(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # check if the user is the owner of the post
    if post.poster_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    # delete the post
    await db.delete(post)
    await db.commit()
    
    return {"message": "Post deleted successfully"}
