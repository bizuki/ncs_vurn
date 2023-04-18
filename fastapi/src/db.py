from typing import Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy import TypeDecorator, MetaData
from contextlib import asynccontextmanager
import config
import asyncio

meta = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
      })

ModelBase: Any = declarative_base(metadata=meta)

class Database:
    def __init__(self, db_url: URL):
        self._engine = create_async_engine(
            db_url,
            future=True,
            pool_size=config.sqlalchemy.pool_size,
            max_overflow=config.sqlalchemy.max_overflow,
            pool_pre_ping=True,
            pool_recycle=600,
        )
        self.__sessionmaker = sessionmaker(
            self._engine,
            expire_on_commit=False,
            class_=AsyncSession,
            future=True
        )
        self._session_factory = async_scoped_session(self.__sessionmaker, scopefunc=asyncio.current_task)

    async def on_startup(self):
        async with self._engine.connect() as conn:
            await conn.run_sync(ModelBase.metadata.reflect)

    @asynccontextmanager
    async def session(self):
        session: AsyncSession = self._session_factory()
        try:
            async with session.begin():
                yield session
        finally:
            await session.close()
