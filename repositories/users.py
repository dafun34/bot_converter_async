from sqlalchemy import insert, select

from repositories.base import Base, Repository
from tables.user import User


class UsersDBClient:

    @classmethod
    async def insert_user(cls,user_id: int):
        query = insert(User).values(id=user_id)
        await Repository.insert(query)

    @classmethod
    async def get_user(cls, user_id: int):
        query = select(User).where(User.id == user_id)
        return await Repository.scalar(query)

    @classmethod
    async def get_all_users(cls):
        query = select(User)
        return await Repository.all(query)
