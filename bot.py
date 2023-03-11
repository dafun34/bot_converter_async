import os
from telegram.ext import ApplicationBuilder, CommandHandler
from dotenv import load_dotenv
from config import settings

load_dotenv()


async def start(update, context):
    await update.effective_chat.send_message(text="Hello, I'm your bot!")

if __name__ == '__main__':
    help = "Run a bot."

    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)
    application.run_polling()