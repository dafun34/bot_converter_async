from sqlalchemy import select, insert

from repositories.base import Base
from repositories.base import Repository
from tables.user import User


async def insert_user(user_id: int):
    query = insert(User).values(id=user_id)
    await Repository.insert(query)
