from typing import Annotated

from fastapi import APIRouter,Depends
from app.database import SessionLocal
from app.models import User, UserCreate, UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


async def get_db():
    async with SessionLocal() as db:
        yield db


db_dependency = Annotated[AsyncSession, Depends(get_db)]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/")
async def create_user(user: UserCreate, db: db_dependency):
    hashed_password = pwd_context.hash(user.hashed_password)
    new_user = User(**user.model_dump(exclude="password"),
                    hashed_password=hashed_password)
    db.add(new_user)
    
    await db.flush()

    # 5. Create role
    user_role = UserRole(
        user_id=user.id,
        role=user.role
    )
    db.add(user_role)
    await db.commit()
    await db.refresh(new_user)

    return new_user


