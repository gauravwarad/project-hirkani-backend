from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.user import UserFollowers, UserFollowing
from app.models.user import User
from app.schemas.follow import GetUserProfileSchema, Message
from app.models.follow import Follow, FollowRequests
from ..dependencies import get_db
from app.auth import current_active_user

follow_router = APIRouter(tags=["Follow"])


@follow_router.get("/get-profile", response_model=GetUserProfileSchema)
async def get_user_profile(who: str = Query(..., min_length=1), db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    # Fetch user's posts
    result = await db.execute(select(User).filter(User.username == who))
    getuser = result.scalars().first()
    if not getuser:
        raise HTTPException(status_code=404, detail="user not found.")
    stmt = select(Follow).where(Follow.follower_id == user.id, Follow.following_id == getuser.id)
    result = await db.execute(stmt)
    existing_follow = result.scalar_one_or_none()
    
    posts = [
    {
      "id": 1,
      "title": "My First Post",
      "content": "i read the news today oh boy",
      "created_at": "2025-03-06T12:00:00"
    }
    ]
    return GetUserProfileSchema(
        username=getuser.username,
        following=True if existing_follow else False,
        posts=posts
    )

# Follow a user
@follow_router.post("/follow/{user_name}", response_model=Message)
async def follow_user(user_name: str, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    result = await db.execute(select(User).filter(User.username == user_name))
    user_id = result.scalar().id

    if user_id == user.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself.")
    
    stmt = select(Follow).where(Follow.follower_id == user.id, Follow.following_id == user_id)
    result = await db.execute(stmt)
    existing_follow = result.scalar_one_or_none()
    
    if existing_follow:
        raise HTTPException(status_code=400, detail="Already following this user.")

    # follow = Follow(follower_id=user.id, following_id=user_id)
    # db.add(follow)
    # await db.commit()

    follow_request = FollowRequests(sender_id=user.id, receiver_id=user_id)
    db.add(follow_request)
    await db.commit()
    return {"message": "Follow request sent successfully"}

# apis for 1. accepting a follow request, 2. rejecting a follow request, 3. cancelling a sent follow request
@follow_router.post("/accept-follow-request/{user_name}", response_model=Message)
async def accept_follow_request(user_name: str, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    result = await db.execute(select(User).filter(User.username == user_name))
    user_id = result.scalar().id

    if user_id == user.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself.")
    
    stmt = select(FollowRequests).where(FollowRequests.sender_id == user_id, FollowRequests.receiver_id == user.id)
    result = await db.execute(stmt)
    existing_follow_request = result.scalar_one_or_none()
    
    if not existing_follow_request:
        raise HTTPException(status_code=400, detail="No follow request from this user.")

    follow = Follow(follower_id=user_id, following_id=user.id)
    db.add(follow)
    await db.commit()

    await db.delete(existing_follow_request)
    await db.commit()
    
    return {"message": "Follow request accepted successfully"}

@follow_router.delete("/reject-follow-request/{user_name}", response_model=Message)
async def reject_follow_request(user_name: str, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    result = await db.execute(select(User).filter(User.username == user_name))
    user_id = result.scalar().id

    if user_id == user.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself.")
    
    stmt = select(FollowRequests).where(FollowRequests.sender_id == user_id, FollowRequests.receiver_id == user.id)
    result = await db.execute(stmt)
    existing_follow_request = result.scalar_one_or_none()
    
    if not existing_follow_request:
        raise HTTPException(status_code=400, detail="No follow request from this user.")

    await db.delete(existing_follow_request)
    await db.commit()
    
    return {"message": "Follow request rejected successfully"}

@follow_router.delete("/cancel-follow-request/{user_name}", response_model=Message)
async def cancel_follow_request(user_name: str, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    result = await db.execute(select(User).filter(User.username == user_name))
    user_id = result.scalar().id

    if user_id == user.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself.")
    
    stmt = select(FollowRequests).where(FollowRequests.sender_id == user.id, FollowRequests.receiver_id == user_id)
    result = await db.execute(stmt)
    existing_follow_request = result.scalar_one_or_none()
    
    if not existing_follow_request:
        raise HTTPException(status_code=400, detail="No follow request sent to this user.")

    await db.delete(existing_follow_request)
    await db.commit()
    
    return {"message": "Follow request cancelled successfully"}

# Unfollow a user
@follow_router.delete("/unfollow/{user_name}", response_model=Message)
async def unfollow_user(user_name: str, db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    result = await db.execute(select(User).filter(User.username == user_name))
    user_id = result.scalar().id
    q = select(Follow).where(Follow.follower_id == user.id, Follow.following_id==user_id)
    result = await db.execute(q)
    follow = result.scalar_one_or_none()
    if not follow:
        raise HTTPException(status_code=400, detail="You are not following this user.")

    await db.delete(follow)
    await db.commit()
    return {"message": "Unfollowed successfully"}



# Get list of followers
async def get_followers(user_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(User.username).join(Follow, Follow.follower_id == User.id).where(Follow.following_id == user_id)
    result = await db.execute(stmt)
    followers = result.scalars().all()  # Extract list of User objects

    requested1 = select(FollowRequests.sender_id).where(FollowRequests.receiver_id == user_id)
    result = await db.execute(requested1)
    # get username from users table
    requested2 = result.scalars().all()
    requested_users = await db.execute(select(User.username).where(User.id.in_(requested2)))
    requested = requested_users.scalars().all()

    return UserFollowers(
        followers=followers,
        followers_requested=requested
    )

# Get list of people the user is following
async def get_following(user_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(User.username).join(Follow, Follow.following_id == User.id).where(Follow.follower_id == user_id)
    result = await db.execute(stmt)
    following = result.scalars().all()  # Extract list of User objects

    stmt2 = select(User.username).join(FollowRequests, FollowRequests.receiver_id == User.id).where(FollowRequests.sender_id == user_id)
    result = await db.execute(stmt2)
    following2 = result.scalars().all()  # Extract list of User objects
    # print("following2", following2)
    # requested1 = select(FollowRequests.receiver_id).where(FollowRequests.sender_id == user_id)
    # result = await db.execute(requested1)
    # # get username from users table
    # requested2 = result.scalars().all()
    # requested_users = await db.execute(select(User.username).where(User.id.in_(requested2)))
    # requested = requested_users.scalars().all()

    return UserFollowing(
        following=following,
        following_requested=following2
    )