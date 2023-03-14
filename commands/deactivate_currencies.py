"""Модуль команды выполняющей деактивацию валют."""
import asyncio

from repositories.currencies import deactivate_currencies_to_default


async def deactivate_currencies() -> None:
    """Деактивировать ваплюты."""
    await deactivate_currencies_to_default()


async def main() -> None:
    """Выполнить команду."""
    await deactivate_currencies()


if __name__ == "__main__":
    asyncio.run(main())
