"""Модуль репозитория валют."""
import datetime

from sqlalchemy import insert, not_, select, update

from config import settings
from repositories.base import Repository
from tables.currency import Currency


class CurrencyDBClient:
    _repository = Repository

    @classmethod
    async def get_all_currencies(cls) -> list[Currency]:
        """Получить все валюты."""
        query = select(Currency)
        return await cls._repository.all(query)

    @classmethod
    async def get_currency_by_char_code(cls, char_code: str) -> Currency:
        """Получить валюту по коду валюты."""
        query = select(Currency).where(Currency.char_code == char_code)
        return await cls._repository.scalar(query)

    @classmethod
    async def create_currency(cls, currency: dict) -> None:
        """Создать валюту."""
        query = insert(Currency).values(**currency)
        await cls._repository.insert(query)

    @classmethod
    async def update_currencies_values(cls, data: dict) -> None:
        """Обновить курс валюты."""
        query = (
            update(Currency)
            .where(Currency.char_code == data["char_code"])
            .values(value=data["value"], updated_at=data["updated_at"])
        )
        await cls._repository.update(query)

    @classmethod
    async def update_or_create_currencies(cls, currencies_json: dict) -> None:
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
            currency = await cls.get_currency_by_char_code(item["CharCode"])
            if not currency:
                await cls.create_currency(data)
            await cls.update_currencies_values(data)

    @classmethod
    async def set_ordering_by_char_code(
        cls, char_code: str, value: int
    ) -> None:
        """Установить сортировку."""
        query = (
            update(Currency)
            .where(Currency.char_code == char_code)
            .values(ordering_id=value)
        )
        await cls._repository.update(query)

    @classmethod
    async def deactivate_currencies_to_default(cls) -> None:
        """Деактивировать валюты которые не в дефолтном списке."""
        query = (
            update(Currency)
            .where(not_(Currency.char_code.in_(settings.ACTIVE_CURRENCIES)))
            .values(is_active=False)
        )
        await Repository.update(query)

    @classmethod
    async def get_all_active_currencies(cls) -> list:
        """Получить список активных валют."""
        query = select(Currency).where(Currency.is_active == True)  # noqa E712
        return await Repository.all(query)

    @classmethod
    async def insert_ruble(cls) -> None:
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


async def write_currencies_sql_query():
    currencies_data = []
    currencies = await CurrencyDBClient.get_all_currencies()
    for curr in currencies:
        currencies_data.append(
            (
                curr.char_code,
                curr.is_active,
                curr.name,
                curr.ordering_id,
                curr.source_id,
                curr.value,
            )
        )
    currencies_data = tuple(currencies_data)
    string_query = (
        f"INSERT INTO currencies (char_code, is_active, name, ordering_id, source_id, value) "
        f"VALUES {currencies_data}"
    )
    pass
