# not the credi card shhh...

import os
from fastapi import APIRouter, Depends, HTTPException, Query
import requests
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.post import CreatePost, PlaceSearch, PlacesSearchResult, SearchRequest
from app.models.user import User
from app.models.business import Business
from app.schemas.follow import Message
from app.schemas.discover import DiscoverListViewObject
from app.models.post import Post
from app.models.follow import Follow
from ..dependencies import get_db
from app.auth import current_active_user

discover_router = APIRouter(tags=["Discover"])


@discover_router.get("/listview", response_model=List[DiscoverListViewObject])
async def list_view(db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):

    # get all following ids of the current user
    # get all businesses ids from the posts from those users
    # get the average rating of those posts
    # get business name, address of those business ids from business table
    # return a list of businesses - business id, name, address, average rating

    result = await db.execute(
        select(Follow.following_id).where(Follow.follower_id == user.id)
    )   
    following_ids = [row[0] for row in result.fetchall()]

    if not following_ids:
        return []

    # calculate average and count of ratings.
    result = await db.execute(
        select(Post.business_id, func.avg(Post.rating).label("average_rating"), func.count(Post.rating).label("num_ratings"))
        .where(Post.poster_id.in_(following_ids))  # Filter by followed users
        .group_by(Post.business_id)
    )

    avg_ratings = {row[0]: (row[1], row[2]) for row in result.fetchall()}

    # get business ids
    business_ids = list(avg_ratings.keys())
    if not business_ids:
        return []
    # get business names and addresses
    result = await db.execute(
        select(Business.id, Business.name, Business.address)
        .where(Business.id.in_(business_ids))
    )
    businesses = result.fetchall()

    # print("executed and found businesses")
    # print(businesses)

    response = [
        DiscoverListViewObject(
            business_id=str(business.id),
            business_name=business.name if business.name else "",
            business_address=business.address if business.address else "",
            business_rating=avg_ratings[business.id][0] if avg_ratings.get(business.id) else 0,
            ratings=avg_ratings[business.id][1] if avg_ratings.get(business.id) else 0,
        )
        for business in businesses
    ]

    return response