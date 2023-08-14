"""Модуль логгера."""
import sys

from loguru import logger
logger = logger

logger.add(sink=sys.stderr, format="{time} {level} {message}", filter="bot_converter_async", level="INFO")


