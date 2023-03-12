"""Утилиты для обработки валютных кооманд."""
import asyncio
import json
from datetime import datetime
from aiohttp import ClientSession, web

from repositories.currencies import update_or_create_currencies


async def get_currencies_for_db() -> None:
    """Получить/обновить курсы валют."""
    async with ClientSession() as session:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        async with session.get(url) as response:
            currencies_json = json.loads(await response.text())['Valute']
            await update_or_create_currencies(currencies_json)

    # response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    # for item in response.json()["Valute"].values():
    #     currency, created = Currencies.objects.get_or_create(
    #         source_id=item["ID"],
    #     )
    #     if created:
    #         currency.name = item["Name"]
    #         currency.char_code = item["CharCode"]
    #         currency.value = item["Value"]
    #         currency.value_updated_at = datetime.now(tz=pytz.UTC)
    #         currency.save()
    #     currency.value = item["Value"]
    #     currency.value_updated_at = datetime.now(tz=pytz.UTC)
    #     currency.save()
    #
    # Currencies.objects.get_or_create(
    #     name="Российский Рубль",
    #     char_code="RUB",
    #     value=float(1),
    #     is_active=True,
    #     ordering_id=1,
    # )


async def main():
    task = asyncio.create_task(get_currencies_for_db())
    await task

if __name__ == '__main__':
    asyncio.run(main())