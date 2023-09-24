from sqlalchemy import insert, select

from repositories.base import Base, Repository
from tables.user import User


class UsersDBClient:

    @classmethod
    async def insert_user(cls, user_id: int) -> int:
        query = insert(User).values(id=user_id)
        cursor = await Repository.insert(query)
        inserted_id = cursor.inserted_primary_key[0]
        return inserted_id

    @classmethod
    async def get_or_create(cls, user_id: int) -> User:
        if user := await cls.get_user(user_id):
            return user
        inserted_id = await cls.insert_user(user_id)
        user = await cls.get_user(inserted_id)
        return user

    @classmethod
    async def get_user(cls, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        return await Repository.scalar(query)

    @classmethod
    async def get_all_users(cls):
        query = select(User)
        return await Repository.all(query)
