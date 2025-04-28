# not the credi card shhh...

import os
from fastapi import APIRouter, Depends, HTTPException, Query
import requests
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.business import GetBusinessProfileObject, BusinessPosts, BusinessHandlerCheck, ClaimBusiness, NewBusinessPost
from app.models.user import User
from app.models.business import Business
from app.schemas.follow import Message
from app.models.business import Business, BusinessPost
from app.models.post import Post
from app.models.follow import Follow
from app.models.business import BusinessFollow
from ..dependencies import get_db
from app.auth import current_active_user

business_router = APIRouter(tags=["Business"])

# api to check if a user is a business handler
@business_router.get("/is_business_handler", response_model=BusinessHandlerCheck)
async def is_business_handler(db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    # Check if the user is a business handler
    result = await db.execute(select(Business).filter(Business.handler_id == user.id))
    business = result.scalar_one_or_none()

    if business:
        return BusinessHandlerCheck(
            answer=True,
            business_id=str(business.id),
        )
    else:
        return BusinessHandlerCheck(
            answer=False,
            business_id="",
        )


# claim business api -> a user can claim a business, with parameter - google_id
@business_router.post("/claim-business", response_model=Message)
async def claim_business(request: ClaimBusiness, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    # Check if the business already exists
    result = await db.execute(select(Business).filter(Business.google_id == request.google_id))
    business = result.scalar_one_or_none()

    if business:
        # if business handler id is taken by someone else, raise an error
        if business.handler_id and business.handler_id != user.id:
            raise HTTPException(status_code=400, detail="Business is already claimed by another user.")
        # Business already exists, update the handler_id
        business.handler_id = user.id
        db.add(business)
        await db.commit()
        return {"message": "Business claimed successfully."}
    else:
        # Business does not exist, create a new entry
        new_business = Business(google_id=request.google_id, handler_id=user.id, name=request.name, address=request.address)
        db.add(new_business)
        await db.commit()
        return {"message": "Business claimed successfully."}

# api to follow a business
@business_router.post("/follow_business/{business_id}", response_model=Message)
async def follow_business(business_id: str, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    # Check if the business exists
    result = await db.execute(select(Business).filter(Business.id == business_id))
    business = result.scalar_one_or_none()

    if not business:
        raise HTTPException(status_code=404, detail="Business not found.")

    # Check if the user is already following the business
    existing_follow = await db.execute(
        select(BusinessFollow).filter(
            BusinessFollow.business_id == business_id,
            BusinessFollow.follower_id == user.id
        )
    )
    if existing_follow.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already following this business.")

    # Create a new follow entry
    follow_entry = BusinessFollow(business_id=business_id, follower_id=user.id)
    db.add(follow_entry)
    await db.commit()
    # Increase the followers count in the business table
    business.followers_count += 1
    await db.commit()
    return {"message": "Successfully followed the business."}

# api to unfollow a business
@business_router.post("/unfollow_business/{business_id}", response_model=Message)
async def unfollow_business(business_id: str, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    # Check if the business exists
    result = await db.execute(select(Business).filter(Business.id == business_id))
    business = result.scalar_one_or_none()

    if not business:
        raise HTTPException(status_code=404, detail="Business not found.")

    # Check if the user is following the business
    existing_follow_result = await db.execute(
        select(BusinessFollow).filter(
            BusinessFollow.business_id == business_id,
            BusinessFollow.follower_id == user.id
        )
    )
    existing_follow = existing_follow_result.scalar_one_or_none()
    if not existing_follow:
        raise HTTPException(status_code=400, detail="Not following this business.")
    print("id", existing_follow.id)
    # Delete the follow entry
    await db.delete(existing_follow)
    await db.commit()
    # Decrease the followers count in the business table
    business.followers_count -= 1
    await db.commit()
    return {"message": "Successfully unfollowed the business."}

# api to get business profile - returns name, address, followers count, is it followed by the user, posts, average rating among your friends
@business_router.get("/business_profile/{business_id}", response_model=GetBusinessProfileObject)
async def get_business_profile(business_id: str, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    # Check if the business exists
    result = await db.execute(select(Business).filter(Business.id == business_id))
    business = result.scalar_one_or_none()

    if not business:
        raise HTTPException(status_code=404, detail="Business not found.")
    print("business id", business.id)
    # get posts from the from business_posts table
    posts_result = await db.execute(
        select(BusinessPost).filter(BusinessPost.business_id == business_id).order_by(BusinessPost.created_at.desc())
    )
    all_posts = posts_result.scalars().all()
    posts = []
    for post in all_posts:
        posts.append(BusinessPosts(
            id=post.id,
            title=post.title,
            content=post.content,
            posted_at=post.created_at
        ))
    print("posts", posts)

    # is it followed by the user
    is_followed = await db.execute(
        select(BusinessFollow).filter(
            BusinessFollow.business_id == business_id,
            BusinessFollow.follower_id == user.id
        )
    )
    is_followed = is_followed.scalar_one_or_none() is not None

    # calculate average ratings among friends and number of ratings from friends
    result = await db.execute(
        select(func.avg(Post.rating).label("average_rating"), func.count(Post.rating).label("num_ratings"))
        .where(Post.business_id == business_id)
        .where(Post.poster_id.in_(
            select(Follow.follower_id).where(Follow.following_id == user.id)
        ))
        .group_by(Post.business_id)
    )
    avg_rating = result.scalar_one_or_none()

    average_rating = avg_rating[0] if avg_rating else 0
    num_ratings = avg_rating[1] if avg_rating else 0

    return GetBusinessProfileObject(
        name=business.name if business.name else "",
        address=business.address if business.address else "",
        followers_count=business.followers_count,
        posts=posts,
        average_rating=average_rating,
        num_ratings=num_ratings,
        is_followed=is_followed,
        is_handler=business.handler_id == user.id
    )


# api to post as a business. saves to the business_posts table, request body - title, content, business_id (NewBusinessPost)
@business_router.post("/post_business", response_model=Message)
async def post_business(request: NewBusinessPost, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    # Check if the business exists
    result = await db.execute(select(Business).filter(Business.id == request.business_id))
    business = result.scalar_one_or_none()

    if not business:
        raise HTTPException(status_code=404, detail="Business not found.")

    # Check if the user is the handler of the business
    if business.handler_id != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to post for this business.")

    # Create a new post entry
    new_post = BusinessPost(title=request.title, content=request.content, business_id=request.business_id)
    db.add(new_post)
    await db.commit()
    return {"message": "Post created successfully."}


# api to save a new business to db
@business_router.post("/save-business", response_model=BusinessHandlerCheck)
async def save_business(request: ClaimBusiness, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    # Check if the business already exists
    result = await db.execute(select(Business).filter(Business.google_id == request.google_id))
    business = result.scalar_one_or_none()

    if business:
        # raise HTTPException(status_code=400, detail="Business already exists.")
        return BusinessHandlerCheck(
            answer=True,
            business_id=str(business.id),
        )
    else:
        # Business does not exist, create a new entry
        new_business = Business(google_id=request.google_id, name=request.name, address=request.address)
        db.add(new_business)
        await db.commit()
        # return {"message": "Business saved successfully."}
        result = await db.execute(select(Business).filter(Business.google_id == request.google_id))
        business = result.scalar_one_or_none()
        return BusinessHandlerCheck(
            answer=True,
            business_id=str(business.id),
        )


