from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
class Business(Base):
    __tablename__ = "business"
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    google_id = Column(String)
    handler_id = Column(UUID, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    followers_count = Column(Integer, default=0)

class BusinessFollow(Base):
    __tablename__ = "business_follow"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(UUID, ForeignKey("business.id", ondelete="CASCADE"), nullable=False)
    follower_id = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=func.now())

class BusinessPost(Base):
    __tablename__ = "business_post"
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(UUID, ForeignKey("business.id", ondelete="CASCADE"), nullable=False)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=func.now())

