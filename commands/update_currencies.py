"""Модуль команды получающей и обновляющей валюты."""
import asyncio
import json

from aiohttp import ClientSession

from repositories.currencies import CurrencyDBClient


async def get_currencies_for_db() -> None:
    """Получить/обновить курсы валют."""
    async with ClientSession() as session:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        async with session.get(url) as response:
            currencies_json = json.loads(await response.text())["Valute"]
            await CurrencyDBClient.update_or_create_currencies(currencies_json)


async def main() -> None:
    """Запустить команду."""
    await get_currencies_for_db()


if __name__ == "__main__":
    asyncio.run(main())
