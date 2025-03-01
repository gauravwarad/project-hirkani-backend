from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import settings

# Use async engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

# Dependency for FastAPI (async session)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
