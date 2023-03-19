"""Модуль приложения."""
import os

from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from handlers.callback import (
    detail_currency_handler,
    get_currencies_handler,
    help_callback_handler,
    menu_callback_handler,
)
from handlers.command import start
from handlers.convert_scenario import (
    ConvertState,
    cancel,
    converter_scenario_entry_point,
    get_first_currency_for_convert,
    output_convert_result,
    set_first_currency,
)
from log.logger import logger

load_dotenv()


if __name__ == "__main__":
    logger.info("Bot run up.")
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
            ConvertState.VALUE_FOR_CONVERT.value: [
                MessageHandler(
                    filters.TEXT,
                    get_first_currency_for_convert,
                ),
            ],
            ConvertState.CONVERTED_CURRENCY.value: [
                CallbackQueryHandler(set_first_currency, pattern="^[A-Z]{3}")
            ],
            ConvertState.TO_CONVERT_CURRENCY.value: [
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
    application.add_handler(
        CallbackQueryHandler(
            help_callback_handler, pattern="^help_callback_handler"
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            menu_callback_handler, pattern="^menu_callback_handler"
        )
    )
    application.add_handler(
        CallbackQueryHandler(
            get_currencies_handler, pattern="^get_currencies_handler"
        )
    )
    application.add_handler(
        CallbackQueryHandler(detail_currency_handler, pattern="^[A-Z]{3}")
    )
    application.run_polling()

    application.run_polling()
