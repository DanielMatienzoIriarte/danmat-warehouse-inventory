import contextlib
from collections.abc import AsyncIterator
from typing import Any, AsyncGenerator
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from src.database.models import product

db_url = "postgresql+asyncpg://salesman:salesman@locahost:5432/warehouse"


class Base(DeclarativeBase):
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession
    __mapper_args__ = {"eager_defaults": True}


class DatabaseSessionManager:
    def __init__(self, engine_kwargs=None):
        if engine_kwargs is None:
            engine_kwargs = {}

        #self._engine = create_async_engine(db_url, **engine_kwargs)
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

    @contextlib.asynccontextmanager
    async def create_db_pool(self) -> AsyncIterator[AsyncSession]:
        if self.db_local_session is None:
            raise RuntimeError("Database engine not initialized")

        session = self.db_local_session()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    @contextlib.asynccontextmanager
    async def get_db_pool(self) -> AsyncGenerator[AsyncSession, Any]:
        db = self.db_local_session

        async with db() as session:
            yield session

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncSession]:
        if self._engine is None:
            raise Exception("Database Engine is not initialized")

        session = self.db_local_session()
        async with session as conn:
            try:
                yield conn
            except Exception:
                await conn.rollback()
                raise

    @contextlib.asynccontextmanager
    async def close(self):
        if self._engine is None:
            raise Exception("Database Engine is not initialized")

        await self._engine.dispose()

        self._engine = None
        self.db_local_session = None

    @contextlib.asynccontextmanager
    async def get_connection(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("Database Engine is not initialized")

        connection = await self.connect(self)
        try:
            yield connection
        finally:
            await connection.close()

    async def create_tables(self):
        async with self.get_connection(self) as conn:
            await conn.run_sync(Base.metadata.create_all)

        await self._engine.dispose()
