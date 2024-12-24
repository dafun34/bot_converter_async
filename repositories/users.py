import os

from sqlalchemy import insert, select

from repositories.base import Base, Repository
from tables.user import User


class UsersDBClient:
    @classmethod
    async def insert_user(cls, user_id: int, is_admin: bool) -> int:
        query = insert(User).values(id=user_id, is_admin=is_admin)
        cursor = await Repository.insert(query)
        inserted_id = cursor.inserted_primary_key[0]
        return inserted_id

    @classmethod
    def is_admin(cls, user_id: int):
        is_admin = False
        prefix = "ADMIN_ID_"
        variable_names = [
            value
            for key, value in os.environ.items()
            if key.startswith(prefix)
        ]
        if str(user_id) in variable_names:
            is_admin = True
        return is_admin

    @classmethod
    async def get_or_create(cls, user_id: int) -> User:
        # TODO Сейчас захардкожен только 1 админ
        is_admin = cls.is_admin(user_id)
        if user := await cls.get_user(user_id):
            return user
        inserted_id = await cls.insert_user(user_id=user_id, is_admin=is_admin)
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
