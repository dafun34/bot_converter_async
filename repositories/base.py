
from typing import Any, NewType, Union

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Delete, Insert, Select, Update

from db import async_session
from tables.base import Base

Query = NewType("Query", Union[Delete, Select, Update, Insert])


class Repository:
    """Класс обертка для работы с базой."""

    @classmethod
    async def _execute(cls, query: Query) -> Result:
        """Обернуть запрос в сессию."""
        async with async_session() as session:
            cursor = await cls._db_request(session, query=query)
            await session.commit()
            return cursor

    @classmethod
    async def all(cls, query: Query) -> list[Any]:
        """Получить все записи из базы как сущность таблицы."""
        return [result[0] for result in (await cls._execute(query)).all()]

    @classmethod
    async def scalar(cls, query: Query) -> tuple[Any, ...]:
        """Получить одну запись из базы."""
        return (await cls._execute(query)).scalar()

    @classmethod
    async def insert(cls, query: Query) -> Any:
        """Добавить запись в базу."""
        return await cls._execute(query)

    @classmethod
    async def bulk_insert(cls, objects: list[Base]) -> Any:
        """Добавить запись в базу."""
        async with async_session() as session:
            session.add_all(objects)
            await session.commit()

    @classmethod
    async def update(cls, query: Query) -> Any:
        """Обновить запись в базе."""
        return await cls._execute(query)

    @classmethod
    async def delete(cls, query: Query) -> Any:
        """Обновить запись в базе."""
        return await cls._execute(query)

    @classmethod
    async def _db_request(
            cls, session: AsyncSession, *, query: Query
    ) -> Result:
        """Выполнить запрос в базу."""
        raw_query = query
        if hasattr(query, "statement"):
            raw_query = query.statement

        return await session.execute(raw_query)
