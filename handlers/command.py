"""Модуль обработчиков команд."""
from telegram import Update
from telegram.ext import ContextTypes

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
    await update.message.reply_text(text, reply_markup=start_markup())
