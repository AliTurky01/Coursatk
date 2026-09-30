from fastapi import FastAPI
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Fetch URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Force standard engine creation (if using sync drivers like psycopg2)
# engine = create_engine(DATABASE_URL)

# IF USING ASYNCPG (Async setup):
# Make sure your .env uses: postgresql+asyncpg://...
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@app.get("/")
def root():
    return {"message": "Coursatk API is running"}
