"""Модуль обработчиков команд."""
from telegram import Update
from telegram.ext import ContextTypes

from commands.update_currencies import get_currencies_for_db
from log.logger import logger
from markups.markups import start as start_markup
from repositories.users import UsersDBClient


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды старт.

    Здесь выводится приветствие. Инлайн клавиатура в которой есть.
    Помощь.
    Меню.
    ...
    """
    logger.info(
        f"User with ID {update.effective_user.id} execute start command"
    )
    text = (
        f"Привет {update.effective_user.name} "
        f"я бот конвертер, с моими возможностями "
        f"можно ознакомиться в пункете Помощь"
    )
    logger.info(
        f"User with name: {update.effective_user.name} "
        f"and id {update.effective_user.id} executed a start"
    )
    await UsersDBClient.get_or_create(update.effective_user.id)
    await update.message.reply_text(text, reply_markup=start_markup())


async def update_currencies(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    logger.info(
        f"User with ID {update.effective_user.id} try execute update_currencies"
    )

    user = await UsersDBClient.get_user(update.effective_user.id)

    if user and user.is_admin:
        await get_currencies_for_db()
        await update.message.reply_text("Курсы обновлены")
    else:
        await update.message.reply_text(
            "У вас нет прав админа, или не удалось получить юзера из БД"
        )
