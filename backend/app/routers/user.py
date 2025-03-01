from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_db

router = APIRouter()


@router.get("/users/")
async def get_users(db: AsyncSession = Depends(get_db)):
    # Example: Fetch users from DB (Replace with actual query)
    return {"message": "List of users"}
