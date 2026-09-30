from fastapi import FastAPI
import os
from sqlalchemy import create_engine

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm import Session, defer
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from pydantic import BaseModel
from .database import Base,SessionLocal
from .models import Department, User, UserRole, Employee, Student, Course, Instruction, Enroll
app = FastAPI()



async def get_db():
    async with SessionLocal() as db:
        yield db


db_dependency = Annotated[AsyncSession, Depends(get_db)]


class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    department_id: int | None = None



@app.post("/users/")
async def create_user(user: UserCreate, db: db_dependency):
    user = User(**user.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@app.get("/")
def root():
    return {"message": "Coursatk API is running"}
