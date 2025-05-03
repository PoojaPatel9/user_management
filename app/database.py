# app/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.base import Base  # ✅ your Base is imported from a separate file
import asyncio

class Database:
    """Handles database connections and sessions."""
    _engine = None
    _session_factory = None

    @classmethod
    def initialize(cls, database_url: str, echo: bool = False):
        """Initialize the async engine and sessionmaker."""
        if cls._engine is None:
            cls._engine = create_async_engine(database_url, echo=echo, future=True)
            cls._session_factory = sessionmaker(
                bind=cls._engine, class_=AsyncSession, expire_on_commit=False, future=True
            )

    @classmethod
    def get_session_factory(cls):
        """Returns the session factory, ensuring it's initialized."""
        if cls._session_factory is None:
            raise ValueError("Database not initialized. Call `initialize()` first.")
        return cls._session_factory

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            raise ValueError("Database not initialized. Call `initialize()` first.")
        return cls._engine


# ✅ Optional: Add this function only if you really need to manually create tables
async def init_db():
    engine = Database.get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
