import os
from fastapi import APIRouter, Depends, HTTPException, Query
import requests
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.post import CreatePost, PlaceSearch, PlacesSearchResult, SearchRequest
from app.models.user import User
from app.models.business import Business
from app.schemas.follow import Message
from app.schemas.homepage import HomePagePostRequest, PostSchema
from app.models.post import Post
from app.models.follow import Follow
from ..dependencies import get_db
from app.auth import current_active_user

home_router = APIRouter(tags=["HomePage"])


@home_router.post("/home", response_model=List[PostSchema])
async def get_home(request: HomePagePostRequest, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    
    # get all following ids of the current user
    # get all posts from those users
    # pagination?
    # show those posts with latest posts first

    """Fetch home feed: posts from followed users, sorted by latest."""

    # 🔹 1. Get all user IDs that the current user follows
    result = await db.execute(
        select(Follow.following_id).where(Follow.follower_id == user.id)
    )
    following_ids = [row[0] for row in result.fetchall()]

    if not following_ids:
        return []  # Return an empty list if the user follows no one
    skip = request.skip
    limit = request.limit
    # 🔹 2. Fetch posts from followed users, sorted by latest first
    result = await db.execute(
        select(Post)
        .where(Post.poster_id.in_(following_ids))  # Filter by followed users
        .order_by(desc(Post.created_at))  # Sort by latest posts first
        .offset(skip)  # Pagination: Skip `skip` number of posts
        .limit(limit)  # Pagination: Limit results to `limit` posts
        .options(joinedload(Post.poster))  # Eager load user data, maybe can be used later; not relevant for now
    )

    posts = result.scalars().all()
    posts = [
        {
          "id": post.id,
          "title": post.title,
          "content": post.text,
          "rating": post.rating,
          "created_at": post.created_at.isoformat()
      }
      for post in posts
    ]
    return posts  # Return list of Post objects