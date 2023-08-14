"""Модуль логгера."""
import sys

from loguru import logger
logger = logger

logger.add(level="INFO", sink=sys.stderr, colorize=True, format="{level} <light-blue>{time}</light-blue> <level>{message}</level>")
