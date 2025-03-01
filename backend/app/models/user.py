from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Integer, String, Column
# from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    # id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # username: Mapped[str] = mapped_column(String(length=64), unique=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    # FastAPI-Users automatically includes email, hashed_password, is_active, and is_superuser
    pass