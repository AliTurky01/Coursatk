from fastapi import FastAPI,APIRouter
import os
from sqlalchemy import create_engine

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm import Session, defer
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.routers import users,departments,courses
from .database import Base,SessionLocal
from .models import Department, User, UserRole, Employee, Student, Course, Instruction, Enroll

app = FastAPI()
app.include_router(users.router)
# app.include_router(courses.router)
# app.include_router(departments.router)



async def get_db():
    async with SessionLocal() as db:
        yield db


db_dependency = Annotated[AsyncSession, Depends(get_db)]







