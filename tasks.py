
import os

import telegram

from repositories.users import get_all_users

from dotenv import load_dotenv

load_dotenv()


async def send_test_messages():
    bot = telegram.Bot(token=os.getenv("BOT_TOKEN"))
    users = await get_all_users()
    async with bot:
        try:
            await bot.initialize()
            for user in users:
                await bot.send_message(chat_id=user.id, text="Привет")
        finally:
            await bot.shutdown()
