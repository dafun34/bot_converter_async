"""Модуль обработчиков Callback запросов."""
import inspect
import sys

import telegram.ext
from morph_analyzer import MorphParser
from telegram import CallbackQuery, Update

from markups.markups import active_currencies_markup
from markups.markups import menu as menu_markup
from markups.markups import start
from repositories.currencies import (
    get_all_active_currencies_values,
    get_currency_by_char_code,
)
from tables.currencies import Currencies


async def help_callback_handler(update: Update, query: CallbackQuery) -> None:
    """Обработчик запроса get_help.

    Выводит помощь и инлайн клавиатуру
    """
    await query.answer()
    text = "Тут будет help"
    await update.effective_chat.send_message(text, reply_markup=start())


async def menu_callback_handler(update: Update, query: CallbackQuery) -> None:
    """Обработчик запроса get_menu.

    Возвращает инлайн клавиатуру.
    В которой есть:
    "Курсы валют"
    ...
    """
    await query.answer()
    await update.effective_chat.send_message(
        "Меню:", reply_markup=menu_markup()
    )


async def get_currencies_handler(
    update: Update,
    query: CallbackQuery,
) -> None:
    """
    Обработчик запроса get_currencies.

    Возвращает инлайн клавиатуру активных курсов валют.

    """
    await query.answer()
    currencies = await get_all_active_currencies_values()
    reply_markup = active_currencies_markup(currencies)
    await update.effective_chat.send_message(
        text="Активные валюты:", reply_markup=reply_markup
    )


async def base_handler(
    update: Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE
) -> None:
    """Базовый хендлер."""
    query = update.callback_query
    handler = CALLBACK_HANDLERS.get(query.data)
    await handler(update, query)


async def detail_currency_handler(
    update: Update,
    query: CallbackQuery,
) -> None:
    """Обработчик получения курса по запросу с кнопки."""
    await query.answer()
    morph_parser = MorphParser()
    char_code = update.callback_query.data
    currency = await get_currency_by_char_code(char_code)
    currency_name = morph_parser.change_case(currency.name)
    updated_at = currency.value_updated_at.strftime("%d-%m-%Y")
    text = f"Курс {currency_name} - {currency.value} от {updated_at}"
    currencies = await get_all_active_currencies_values()
    await update.effective_chat.send_message(
        text, reply_markup=active_currencies_markup(currencies)
    )


def set_handler_by_currency_char_code(handlers: dict) -> dict:
    """Вспомогательная функция для получения активных валют."""
    active_currencies = Currencies.objects.filter(is_active=True).values()
    for currency in active_currencies:
        handlers[currency["char_code"]] = handlers["detail_currency_handler"]
    return handlers


def init_handlers() -> dict:
    """Получить обработчики динамически."""
    name = 0
    func = 1
    handlers = {}
    current_module = sys.modules[__name__]
    for item in inspect.getmembers(current_module, inspect.isfunction):
        if (
            item[name].endswith("handler")
            and callable(item[func])  # noqa W503
            and item[name] != "base_handler"  # noqa W503
        ):
            handlers[item[name]] = item[func]
    handlers = set_handler_by_currency_char_code(handlers)
    return handlers


CALLBACK_HANDLERS = init_handlers()
