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

