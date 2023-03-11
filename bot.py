
import os
from telegram.ext import ApplicationBuilder, CommandHandler
from dotenv import load_dotenv

from db import async_session
from log.logger import logger
from repositories.currencies import get_all_currencies

load_dotenv()


async def start(update, context):
    currencies = await get_all_currencies()
    await update.effective_chat.send_message(text="Hello, I'm your bot!")

if __name__ == '__main__':

    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    logger.info('Bot runed.')
    application.run_polling()
