import os

from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
)

from db import async_session
from handlers.command import start
from log.logger import logger

load_dotenv()


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(
                converter_scenario_entry_point,
                pattern="^start_convert_scenario$",
            )
        ],
        states={
            VALUE_FOR_CONVERT: [
                MessageHandler(
                    filters.TEXT,
                    get_first_currency_for_convert,
                ),
            ],
            CONVERTED_CURRENCY: [
                CallbackQueryHandler(set_first_currency, pattern="^[A-Z]{3}")
            ],
            TO_CONVERT_CURRENCY: [
                CallbackQueryHandler(
                    output_convert_result, pattern="^[A-Z]{3}"
                )
            ],
        },
        fallbacks=[
            CallbackQueryHandler(cancel, pattern="^cancel_convert_scenario")
        ],
    )

    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(base_handler))
    application.run_polling()

    logger.info("Bot run up.")
    application.run_polling()
