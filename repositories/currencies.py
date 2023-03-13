import datetime

from sqlalchemy import insert, select, update

from repositories.base import Repository
from tables.currencies import Currencies


async def get_all_currencies():
    query = select(Currencies)
    return await Repository.all(query)


async def get_currency_by_char_code(char_code):
    query = select(Currencies).where(Currencies.char_code == char_code)
    return await Repository.scalar(query)


async def create_currency(currency: dict):
    query = insert(Currencies).values(**currency)
    await Repository.insert(query)


async def update_currencies_values(values):
    query = (
        update(Currencies)
        .where(Currencies.char_code == values["char_code"])
        .values(value=values["value"], updated_at=values["updated_at"])
    )
    await Repository.update(query)


async def update_or_create_currencies(currencies_json):
    for item in currencies_json.values():
        data = {
            "source_id": item["ID"],
            "char_code": item["CharCode"],
            "name": item["Name"],
            "value": item["Value"],
            "is_active": True,
            "updated_at": datetime.datetime.now(),
        }
        currency = await get_currency_by_char_code(item["CharCode"])
        if not currency:
            await create_currency(data)
        await update_currencies_values(data)


async def set_ordering_by_char_code(char_code, value):
    query = (
        update(Currencies)
        .where(Currencies.char_code == char_code)
        .values(ordering_id=value)
    )
    await Repository.update(query)
    
async def deactivate_currencies_to_default():
    update(Currencies).where(Currencies.char_code)
