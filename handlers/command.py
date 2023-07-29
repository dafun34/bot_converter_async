"""Модуль обработчиков команд."""
from telegram import Update
from telegram.ext import ContextTypes
from log.logger import logger
from markups.markups import start as start_markup


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды старт.

    Здесь выводится приветствие. Инлайн клавиатура в которой есть.
    Помощь.
    Меню.
    ...
    """
    text = (
        f"Привет {update.effective_user.name} "
        f"я бот конвертер, с моими возможностями "
        f"можно ознакомиться в пункете Помощь"
    )
    logger.info(
        f"User with name: {update.effective_user.name} "
        f"and id {update.effective_user.id} executed a start"
    )
    await update.message.reply_text(text, reply_markup=start_markup())
