"""Модуль команды устанавливающей сортировку."""
import asyncio

from repositories.currencies import (
    get_currency_by_char_code,
    set_ordering_by_char_code,
)


async def set_currencies_ordering():
    ordering = {"USD": 2, "EUR": 3, "GBP": 4, "JPY": 5}
    for curr, number in ordering.items():
        currency = await set_ordering_by_char_code(curr, number)


async def main():
    await set_currencies_ordering()


if __name__ == "__main__":
    asyncio.run(main())
