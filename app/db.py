import os
from typing import Annotated

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, mapped_column

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine("postgresql+asyncpg://user:password@localhost/dbname")

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()
