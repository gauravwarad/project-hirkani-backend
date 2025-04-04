from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.user import UserProfileSchema
from app.models.user import User
from app.models.post import Post
from app.routers.follow import get_followers, get_following
from ..dependencies import get_db
from app.auth import current_active_user

user_router = APIRouter()


@user_router.get("/users/")
async def get_users(db: AsyncSession = Depends(get_db)):
    # Example: Fetch users from DB (Replace with actual query)
    return {"message": "List of users"}

@user_router.get("/profile")
async def get_user_profile(db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    
    followers = await get_followers(user.id, db)
    following = await get_following(user.id, db)

    # Fetch user's posts
    result = await db.execute(select(Post).filter(Post.poster_id == user.id))
    posts = result.scalars().all()

    # Format posts for the response
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
  #   posts = [
  #   {
  #     "id": 1,
  #     "title": "My First Post",
  #     "content": "i read the news today oh boy",
  #     "created_at": "2025-03-06T12:00:00"
  #   },
  #   {
  #     "id": 2,
  #     "title": "Not the first Post",
  #     "content": "horses are bikes that pedal themselves.",
  #     "created_at": "2025-03-06T12:00:00"
  #   },
  #   {
  #     "id": 3,
  #     "title": "definitely not the first Post",
  #     "content": "and i think to myself what a wonderful world. the colours of the rainbow so pretty in sky. are also on the faces of people going by. i see friends shaking hands saying how do you do, they are really saying i love you. i hear babies cry i watch them grow they will learn much more than i'll ever know and i think to myself what a wonderful world.",
  #     "created_at": "2025-03-06T12:00:00"
  #   }
  # ]

    return UserProfileSchema(
        username=user.username,
        email=user.email,
        followers=followers,
        following=following,
        posts=posts
    )

# to search for users to follow, idk
@user_router.get("/search", response_model=List[UserProfileSchema])
async def search_users(query: str = Query(..., min_length=1), db: AsyncSession = Depends(get_db), user = Depends(current_active_user)):
    result = await db.execute(select(User).filter(User.username.ilike(f"%{query}%")).limit(10))
    users = result.scalars().all()
    return users
