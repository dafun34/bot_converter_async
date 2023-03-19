"""Модуль логгера."""
import logging as log

log.basicConfig(
    level=log.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = log.getLogger("bot_converter_async")
