import os
import asyncio
import telegram


async def send_test_messages():
    dafun = 452301815
    bot = telegram.Bot(token=os.getenv("BOT_TOKEN"))
    async with bot:
        try:
            await bot.initialize()
            await bot.send_message(chat_id=dafun, text="хуй")
        finally:
            await bot.shutdown()


if __name__ == "__main__":
    asyncio.run(send_test_messages())