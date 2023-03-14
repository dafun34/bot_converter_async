"""Модуль с обработчиками сценария конвертации валют."""
import decimal
import re
from enum import Enum
from typing import Union

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from markups.markups import (
    active_currencies_markup,
    converter_scenario_markup,
    menu,
)
from repositories.currencies import get_all_active_currencies_values


class ConvertState(Enum):
    """Энум со значениями сценария конвертации."""
    VALUE_FOR_CONVERT = 1
    CONVERTED_CURRENCY = 2
    TO_CONVERT_CURRENCY = 3
    REPLACE_VALUE = 4
    CANCEL_VALUE = 5


def add_key_by_char_code_currencies(currencies: dict) -> dict:
    """
    Добавить char_code в качестве ключа.

    Добавляем ключ что бы потом получить по ключу объект валюты.
    """
    cache = {}
    for item in currencies:
        cache[item.char_code] = item
    return cache


async def converter_scenario_entry_point(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Точка входа в сценарий конвертации валют."""
    await update.callback_query.answer()
    text = (
        "Укажите значение которое надо конвертировать.\n"
        "Значение - целое или вещественное число.\n"
    )
    await update.effective_chat.send_message(
        text, reply_markup=converter_scenario_markup()
    )
    return ConvertState.VALUE_FOR_CONVERT.value


async def get_first_currency_for_convert(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Первый этап сценария.

    Обработать введенное значение согласно шаблону.
    Если введеное значение не соответствует шаблону,
    вводить значение придется еще раз пока не введем правильно,
    либо можно отменить сценарий по кнопке.
    """
    pattern = r"^[1-9]\d*(\.\d+)?$"
    if not re.match(pattern, update.message.text):
        text = (
            "Ваш текст не соответствует шаблону\n"
            "Значение должно выглядеть как то так '1.45'\n"
            "Плохие примеры '1,44', '1,45 ', 'привет'"
        )
        await update.effective_chat.send_message(
            text, reply_markup=converter_scenario_markup()
        )
        return ConvertState.VALUE_FOR_CONVERT.value

    value_for_convert = decimal.Decimal(update.message.text)
    context.user_data["value_for_convert"] = value_for_convert
    currencies = await get_all_active_currencies_values()
    currencies = add_key_by_char_code_currencies(currencies)
    context.user_data["active_currencies"] = currencies
    text = (
        "Выберети валюту из которой будет конвертироваться "
        f"это значение: {value_for_convert}"
    )
    await update.effective_chat.send_message(
        text, reply_markup=active_currencies_markup(currencies.values(), True)
    )
    return ConvertState.CONVERTED_CURRENCY.value


async def set_first_currency(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """
    Второй этап сценария.

    Обработать запрос выбора первой валюты.
    """
    await update.callback_query.answer()
    currencies = context.user_data["active_currencies"]
    currency = currencies[update.callback_query.data]
    context.user_data["first_currency"] = currency
    value_for_convert = context.user_data["value_for_convert"]
    text = (
        "Выбирите валюту в которую надо конвертировать "
        f"значение {value_for_convert}"
    )
    await update.effective_chat.send_message(
        text, reply_markup=active_currencies_markup(currencies.values(), True)
    )
    return ConvertState.TO_CONVERT_CURRENCY.value


async def output_convert_result(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Union[ConversationHandler, int]:
    """Получить вторую валюту и вывести результат конвертации."""
    await update.callback_query.answer()
    currencies = context.user_data["active_currencies"]
    first_currency = context.user_data["first_currency"]
    second_currency = currencies[update.callback_query.data]
    value = context.user_data["value_for_convert"]
    output_value = round(
        (first_currency.value / second_currency.value) * value, 2
    )
    text = (
        f"{value} {first_currency.name} = {output_value} "
        f"{second_currency.name}"
    )
    await update.effective_chat.send_message(text, reply_markup=menu())
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Обработчик отмены сценария конвертации."""
    await update.callback_query.answer()
    text = "Запрос об отмене конвертации выполнен"
    await update.effective_chat.send_message(text, reply_markup=menu())
    return ConversationHandler.END
