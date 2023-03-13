import asyncio

from commands.deactivate_currencies import deactivate_currencies
from commands.set_ordering import set_currencies_ordering
from commands.update_currencies import get_currencies_for_db
from repositories.currencies import insert_ruble


async def populate_db():
    await get_currencies_for_db()
    await deactivate_currencies()
    await insert_ruble()
    await set_currencies_ordering()


async def main():
    await populate_db()


if __name__ == "__main__":
    asyncio.run(main())
