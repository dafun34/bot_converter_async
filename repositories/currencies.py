from sqlalchemy import select

from repositories.base import Repository
from tables.currencies import Currencies
from db import async_session


async def get_all_currencies():
    query = select(Currencies)
    return await Repository.all(query)

async def update_or_create_currencies(currencies_json):
    for currency in currencies_json.values():

        pass