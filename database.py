from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from typing import AsyncGenerator
from settings import settings

# Use create_async_engine for async drivers like aiosqlite
engine = create_async_engine(settings.DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

async def create_db_and_tables():
    """Creates all tables defined in SQLModel metadata asynchronously."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provides an async database session dependency for FastAPI routes."""
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False, autocommit=False
    )
    async with async_session() as session:
        yield session