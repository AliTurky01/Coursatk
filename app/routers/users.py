from typing import Annotated

from fastapi import APIRouter,Depends
from app.database import SessionLocal
from app.models import User, UserCreate, UserRole
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter(
    prefix="/users",
    tags=["users"]
)


async def get_db():
    async with SessionLocal() as db:
        yield db


db_dependency = Annotated[AsyncSession, Depends(get_db)]

@router.post("/")
async def create_user(user: UserCreate, db: db_dependency):
    user = User(**user.model_dump())
    db.add(user)
    
    await db.flush()

    # 5. Create role
    user_role = UserRole(
        user_id=user.id,
        role="STUDENT"
    )
    await db.commit()
    await db.refresh(user)

    return user


