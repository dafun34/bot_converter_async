from sqlalchemy import insert, select

from repositories.base import Base, Repository
from tables.user import User


async def insert_user(user_id: int):
    query = insert(User).values(id=user_id)
    await Repository.insert(query)


async def get_all_users():
    query = select(User)
    return await Repository.all(query)
