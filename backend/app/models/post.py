from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Post(Base):
    __tablename__ = "posts"
    # posts table - id, poster (userid), title, text, likes, timestamp
    id = Column(Integer, primary_key=True, index=True)
    poster_id = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    title = Column(String)
    text = Column(String)
    likes = Column(Integer)
    rating = Column(Float)
    business_id = Column(UUID, ForeignKey("business.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime, default=func.now())

    poster = relationship("User", back_populates="posts")

class Likes(Base):
    __tablename__ = "likes"
    # likes table - id, post id, user id
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=func.now())