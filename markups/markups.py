"""Модуль клавиатур бота."""
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def example_inline_markup() -> InlineKeyboardMarkup:
    """Пример инлайн клавиатуры."""
    keyboard_inline = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    return InlineKeyboardMarkup(keyboard_inline)


def example_reply_keyboard() -> ReplyKeyboardMarkup:
    """Пример клавиатуры."""
    keyboard = [
        [KeyboardButton("Option 1"), KeyboardButton("Option 2")],
        [KeyboardButton("Option 3")],
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=True
    )
    return reply_markup


def start() -> InlineKeyboardMarkup:
    """Инлайн кнопки при обработке команды /start."""
    keyboard = [
        [
            InlineKeyboardButton(
                "Помощь",
                callback_data="help_callback_handler",
            )
        ],
        [InlineKeyboardButton("Меню", callback_data="menu_callback_handler")],
    ]
    return InlineKeyboardMarkup(keyboard)


def menu() -> InlineKeyboardMarkup:
    """Клавиатура Меню."""
    keyboard = [
        [
            InlineKeyboardButton(
                "💵 Курсы Валют 💵", callback_data="get_currencies_handler"
            ),
            InlineKeyboardButton(
                "🔄 Конвертер валют 🔄", callback_data="start_convert_scenario"
            ),
            InlineKeyboardButton(
                "📅 VPV Календарь скидок 📅",
                callback_data="get_vpv_calendar_handler",
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def active_currencies_markup(
    currencies: list, converter: bool = False
) -> InlineKeyboardMarkup:
    """
    Получить инлайн кнопки активных валют.

    Возвращает инлайн кнопки отфильтрованых валют(currencies)
    по char_code(Код валюты)
    """
    keyboard = []
    for currency in currencies:
        if not converter and currency.name == "Российский Рубль":
            continue
        keyboard.append(
            [
                InlineKeyboardButton(
                    currency.name,
                    callback_data=currency.char_code,
                )
            ]
        )
    if converter:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "❌ Отменить конвертацию ❌",
                    callback_data="cancel_convert_scenario",
                )
            ]
        )
    else:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "🔝 Вернуться в меню 🔝",
                    callback_data="menu_callback_handler",
                )
            ]
        )
    return InlineKeyboardMarkup(keyboard)


def converter_scenario_markup() -> InlineKeyboardMarkup:
    """
    Илайн клавиатура сценария конвертаци.

    Одна кнопка отмены сценария.
    """
    keyboard = []
    keyboard.append(
        [
            InlineKeyboardButton(
                "❌ Отменить конвертацию ❌",
                callback_data="cancel_convert_scenario",
            )
        ]
    )
    return InlineKeyboardMarkup(keyboard)
