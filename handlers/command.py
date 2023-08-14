"""Модуль обработчиков команд."""
from sqlalchemy.exc import IntegrityError
from telegram import Update
from telegram.ext import ContextTypes
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
    try:
        # TODO Лучше переделать на get_or_create
        await UsersDBClient.insert_user(update.effective_user.id)
    except IntegrityError as err:
        logger.info(f"Error in start command handler {str(err)}")
    await update.message.reply_text(text, reply_markup=start_markup())
