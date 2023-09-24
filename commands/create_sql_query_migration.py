import asyncio

from repositories.currencies import write_currencies_sql_query


async def main():
    result = await write_currencies_sql_query()


if __name__ == "__main__":
    asyncio.run(main())
