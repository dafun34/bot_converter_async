"""Модуль для инициализации БД."""
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings


class DBClient:
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
    )

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    # @classmethod
    # def run_migrations(cls):
    #
