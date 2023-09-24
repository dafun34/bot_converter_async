import asyncio
import os

import telegram
from dotenv import load_dotenv

from repositories.currencies import CurrencyDBClient
from repositories.users import UsersDBClient
from utils.morph_analyzer import MorphParser

load_dotenv()


async def prepare_currency_summary():
    morph_parser = MorphParser()
    text = ""
    active_currencies = await CurrencyDBClient.get_all_active_currencies()
    for currency in active_currencies:
        text += (
            f"Курс {morph_parser.change_case(currency.name)} "
            f"- {currency.value} \n"
        )
    return text


async def send_currencies_summary():
    bot = telegram.Bot(token=os.getenv("BOT_TOKEN"))
    users = await UsersDBClient.get_all_users()
    summary = await prepare_currency_summary()
    async with bot:
        try:
            await bot.initialize()
            for user in users:
                await bot.send_message(chat_id=user.id, text=summary)
        finally:
            await bot.shutdown()


async def main():
    await send_currencies_summary()


if __name__ == "__main__":
    asyncio.run(main())
