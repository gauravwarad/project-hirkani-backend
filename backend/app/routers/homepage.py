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
from app.models.post import Post, Likes
from app.models.business import Business, BusinessPost, BusinessFollow
from app.models.follow import Follow
from ..dependencies import get_db
from app.auth import current_active_user

home_router = APIRouter(tags=["HomePage"])


@home_router.post("/home", response_model=List[PostSchema])
async def get_home(request: HomePagePostRequest, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    
    # get all following ids of the current user
    # get all posts from those users
    # also store the username
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
    posts_data = []
    for post in posts:
        liked = await db.execute(
            select(Likes).filter(Likes.post_id == post.id, Likes.user_id == user.id)
        )
        is_liked = True if liked.scalar_one_or_none() else False
        posts_data.append({
            "id": post.id,
            "title": post.title,
            "content": post.text,
            "rating": post.rating,
            "created_at": post.created_at.isoformat(),
            "username": post.poster.username,
            "likes": post.likes,
            "is_liked": is_liked
        })

    return posts_data  # Return list of Post objects


# like a post
# like: create a new entry in the likes table, update like count in the post table

@home_router.post("/like/{post_id}", response_model=Message)
async def like_post(post_id: int, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    # check if the post exists
    result = await db.execute(select(Post).filter(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # check if the user has already liked the post
    result = await db.execute(select(Post).filter(Post.id == post_id, Post.poster_id == user.id))
    existing_like = result.scalar_one_or_none()
    
    if existing_like:
        raise HTTPException(status_code=400, detail="Already liked this post")
    
    like = Likes(
        user_id=user.id,
        post_id=post_id
    )
    db.add(like)
    await db.commit()
    # update the like count in the post table
    post.likes += 1
    await db.commit()  
    return {"message": "Post liked successfully"}


# unlike a post
# unlike: delete the entry in the likes table, update like count in the post table
@home_router.post("/unlike/{post_id}", response_model=Message)
async def unlike_post(post_id: int, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    # check if the post exists
    result = await db.execute(select(Post).filter(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # check if the user has already liked the post
    result = await db.execute(select(Likes).filter(Likes.post_id == post_id, Likes.user_id == user.id))
    existing_like = result.scalar_one_or_none()
    
    if not existing_like:
        raise HTTPException(status_code=400, detail="Not liked this post")
    print("existing like id", existing_like.id)
    await db.delete(existing_like)
    await db.commit()
    # update the like count in the post table
    post.likes -= 1
    await db.commit()
    return {"message": "Post unliked successfully"}


# create an api similar to /home but for posts from followed businesses.
@home_router.post("/business_home", response_model=List[PostSchema])
async def get_business_feed(request: HomePagePostRequest, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    # get all business ids that the current user follows
    result = await db.execute(
        select(BusinessFollow.business_id).where(BusinessFollow.follower_id == user.id)
    )
    business_ids = [row[0] for row in result.fetchall()]
    if not business_ids:
        return []
    
    # get all posts from those businesses
    skip = request.skip
    limit = request.limit
    result = await db.execute(
        select(BusinessPost)
        .where(BusinessPost.business_id.in_(business_ids))  # Filter by followed businesses
        .order_by(desc(BusinessPost.created_at))  # Sort by latest posts first
        .offset(skip)  # Pagination: Skip `skip` number of posts
        .limit(limit)  # Pagination: Limit results to `limit` posts
    )
    posts = result.scalars().all()
    posts_data = []
    for post in posts:
        # get business name
        business_result = await db.execute(
            select(Business).filter(Business.id == post.business_id)
        )
        business = business_result.scalar_one_or_none()
        if not business:
            raise HTTPException(status_code=404, detail="Business not found")
        posts_data.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at.isoformat(),
            "username": business.name,
            "likes": 0,
            "is_liked": False,
            "rating": 0,
        })
    return posts_data

