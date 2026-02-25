import contextlib
from collections.abc import AsyncIterator
from typing import Any, AsyncGenerator
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine
)

from src.database.models import product

db_url = "postgresql+asyncpg://salesman:salesman@localhost:5432/warehouse"


class DatabaseSessionManager:
    def __init__(self):
        #self._engine = create_async_engine(db_url, **engine_kwargs)
        self._engine: AsyncEngine | None = None
        self.db_local_session: async_sessionmaker[AsyncSession] | None = None

    async def init_db(self):
        self._engine = create_async_engine(
            db_url,
            echo=True,
            future=True,
            pool_size=10,
            max_overflow=20,
        )

        self.db_local_session = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False
        )

    def create_db_pool(self) -> async_sessionmaker[AsyncSession]:
        if self._engine is None:
            raise RuntimeError("Database engine not initialized")

        return self.db_local_session

    async def get_db_pool(self) -> AsyncGenerator[AsyncSession, Any]:
        db = self.db_local_session

        async with db() as session:
            yield session

    async def close(self):
        if self._engine is None:
            raise Exception("Database Engine is not initialized")

        await self._engine.dispose()

        self._engine = None
        self.db_local_session = None

    async def create_tables(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        await self._engine.dispose()