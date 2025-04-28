from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    following_id = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=func.now())

class FollowRequests(Base):
    __tablename__ = "follow_requests"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=func.now())
