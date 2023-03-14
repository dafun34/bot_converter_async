"""Модуль репозитория валют."""
import datetime
import decimal

from sqlalchemy import insert, not_, select, update

from config import settings
from repositories.base import Repository
from tables.currency import Currency


async def get_all_currencies() -> list[Currency]:
    """Получить все валюты."""
    query = select(Currency)
    return await Repository.all(query)


async def get_currency_by_char_code(char_code: str) -> Currency:
    """Получить валюту по коду валюты."""
    query = select(Currency).where(Currency.char_code == char_code)
    return await Repository.scalar(query)


async def create_currency(currency: dict) -> None:
    """Создать валюту."""
    query = insert(Currency).values(**currency)
    await Repository.insert(query)


async def update_currencies_values(data: dict) -> None:
    """Обновить курс валюты."""
    query = (
        update(Currency)
        .where(Currency.char_code == data["char_code"])
        .values(value=data["value"], updated_at=data["updated_at"])
    )
    await Repository.update(query)


async def update_or_create_currencies(currencies_json: dict) -> None:
    """Обновить или записать в БД валюту."""
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


async def set_ordering_by_char_code(
    char_code: str, value: decimal.Decimal
) -> None:
    """Установить сортировку."""
    query = (
        update(Currency)
        .where(Currency.char_code == char_code)
        .values(ordering_id=value)
    )
    await Repository.update(query)


async def deactivate_currencies_to_default() -> None:
    """Деактивировать валюты которые не в дефолтном списке."""
    query = (
        update(Currency)
        .where(not_(Currency.char_code.in_(settings.ACTIVE_CURRENCIES)))
        .values(is_active=False)
    )
    await Repository.update(query)


async def get_all_active_currencies_values() -> list:
    """Получить список активных валют."""
    query = select(Currency).where(Currency.is_active == True)  # noqa E712
    return await Repository.all(query)


async def insert_ruble() -> None:
    """Вставить рубль."""
    query = insert(Currency).values(
        source_id="RUB1",
        name="Российский Рубль",
        char_code="RUB",
        value=1,
        is_active=True,
        ordering_id=1,
    )
    await Repository.insert(query)
