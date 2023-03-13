import asyncio

from repositories.currencies import deactivate_currencies_to_default


async def deactivate_currencies():
    await deactivate_currencies_to_default()


async def main():
    await deactivate_currencies()


if __name__ == "__main__":
    asyncio.run(main())
