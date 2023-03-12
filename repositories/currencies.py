import asyncio
import datetime

from sqlalchemy import insert, select, update
from sqlalchemy.dialects.postgresql import insert as sqlite_upsert

from db import async_session
from repositories.base import Repository
from tables.currencies import Currencies

cur = {
    "AUD": {
        "ID": "R01010",
        "NumCode": "036",
        "CharCode": "AUD",
        "Nominal": 1,
        "Name": "Австралийский доллар",
        "Value": 50.1132,
        "Previous": 50.1718,
    },
    "AZN": {
        "ID": "R01020A",
        "NumCode": "944",
        "CharCode": "AZN",
        "Nominal": 1,
        "Name": "Азербайджанский манат",
        "Value": 44.6709,
        "Previous": 44.6487,
    },
    "GBP": {
        "ID": "R01035",
        "NumCode": "826",
        "CharCode": "GBP",
        "Nominal": 1,
        "Name": "Фунт стерлингов Соединенного королевства",
        "Value": 90.3086,
        "Previous": 89.8461,
    },
    "AMD": {
        "ID": "R01060",
        "NumCode": "051",
        "CharCode": "AMD",
        "Nominal": 100,
        "Name": "Армянских драмов",
        "Value": 19.5632,
        "Previous": 19.5379,
    },
    "BYN": {
        "ID": "R01090B",
        "NumCode": "933",
        "CharCode": "BYN",
        "Nominal": 1,
        "Name": "Белорусский рубль",
        "Value": 26.6758,
        "Previous": 26.6578,
    },
    "BGN": {
        "ID": "R01100",
        "NumCode": "975",
        "CharCode": "BGN",
        "Nominal": 1,
        "Name": "Болгарский лев",
        "Value": 40.9781,
        "Previous": 40.9224,
    },
    "BRL": {
        "ID": "R01115",
        "NumCode": "986",
        "CharCode": "BRL",
        "Nominal": 1,
        "Name": "Бразильский реал",
        "Value": 14.7888,
        "Previous": 14.7717,
    },
    "HUF": {
        "ID": "R01135",
        "NumCode": "348",
        "CharCode": "HUF",
        "Nominal": 100,
        "Name": "Венгерских форинтов",
        "Value": 20.9873,
        "Previous": 21.1299,
    },
    "VND": {
        "ID": "R01150",
        "NumCode": "704",
        "CharCode": "VND",
        "Nominal": 10000,
        "Name": "Вьетнамских донгов",
        "Value": 32.1251,
        "Previous": 32.1078,
    },
    "HKD": {
        "ID": "R01200",
        "NumCode": "344",
        "CharCode": "HKD",
        "Nominal": 10,
        "Name": "Гонконгских долларов",
        "Value": 96.9248,
        "Previous": 96.8642,
    },
    "GEL": {
        "ID": "R01210",
        "NumCode": "981",
        "CharCode": "GEL",
        "Nominal": 1,
        "Name": "Грузинский лари",
        "Value": 29.2834,
        "Previous": 29.2237,
    },
    "DKK": {
        "ID": "R01215",
        "NumCode": "208",
        "CharCode": "DKK",
        "Nominal": 1,
        "Name": "Датская крона",
        "Value": 10.7696,
        "Previous": 10.7563,
    },
    "AED": {
        "ID": "R01230",
        "NumCode": "784",
        "CharCode": "AED",
        "Nominal": 1,
        "Name": "Дирхам ОАЭ",
        "Value": 20.677,
        "Previous": 20.6656,
    },
    "USD": {
        "ID": "R01235",
        "NumCode": "840",
        "CharCode": "USD",
        "Nominal": 1,
        "Name": "Доллар США",
        "Value": 75.9406,
        "Previous": 75.9028,
    },
    "EUR": {
        "ID": "R01239",
        "NumCode": "978",
        "CharCode": "EUR",
        "Nominal": 1,
        "Name": "Евро",
        "Value": 80.4009,
        "Previous": 80.1372,
    },
    "EGP": {
        "ID": "R01240",
        "NumCode": "818",
        "CharCode": "EGP",
        "Nominal": 10,
        "Name": "Египетских фунтов",
        "Value": 24.5867,
        "Previous": 24.5904,
    },
    "INR": {
        "ID": "R01270",
        "NumCode": "356",
        "CharCode": "INR",
        "Nominal": 100,
        "Name": "Индийских рупий",
        "Value": 92.3129,
        "Previous": 91.9415,
    },
    "IDR": {
        "ID": "R01280",
        "NumCode": "360",
        "CharCode": "IDR",
        "Nominal": 10000,
        "Name": "Индонезийских рупий",
        "Value": 49.1907,
        "Previous": 49.1248,
    },
    "KZT": {
        "ID": "R01335",
        "NumCode": "398",
        "CharCode": "KZT",
        "Nominal": 100,
        "Name": "Казахстанских тенге",
        "Value": 17.2154,
        "Previous": 17.3069,
    },
    "CAD": {
        "ID": "R01350",
        "NumCode": "124",
        "CharCode": "CAD",
        "Nominal": 1,
        "Name": "Канадский доллар",
        "Value": 55.0693,
        "Previous": 55.0619,
    },
    "QAR": {
        "ID": "R01355",
        "NumCode": "634",
        "CharCode": "QAR",
        "Nominal": 1,
        "Name": "Катарский риал",
        "Value": 20.8628,
        "Previous": 20.8524,
    },
    "KGS": {
        "ID": "R01370",
        "NumCode": "417",
        "CharCode": "KGS",
        "Nominal": 100,
        "Name": "Киргизских сомов",
        "Value": 86.8687,
        "Previous": 86.8254,
    },
    "CNY": {
        "ID": "R01375",
        "NumCode": "156",
        "CharCode": "CNY",
        "Nominal": 1,
        "Name": "Китайский юань",
        "Value": 10.8995,
        "Previous": 10.8623,
    },
    "MDL": {
        "ID": "R01500",
        "NumCode": "498",
        "CharCode": "MDL",
        "Nominal": 10,
        "Name": "Молдавских леев",
        "Value": 40.4538,
        "Previous": 40.4244,
    },
    "NZD": {
        "ID": "R01530",
        "NumCode": "554",
        "CharCode": "NZD",
        "Nominal": 1,
        "Name": "Новозеландский доллар",
        "Value": 46.3693,
        "Previous": 46.3614,
    },
    "NOK": {
        "ID": "R01535",
        "NumCode": "578",
        "CharCode": "NOK",
        "Nominal": 10,
        "Name": "Норвежских крон",
        "Value": 71.2495,
        "Previous": 71.2147,
    },
    "PLN": {
        "ID": "R01565",
        "NumCode": "985",
        "CharCode": "PLN",
        "Nominal": 1,
        "Name": "Польский злотый",
        "Value": 17.1741,
        "Previous": 17.147,
    },
    "RON": {
        "ID": "R01585F",
        "NumCode": "946",
        "CharCode": "RON",
        "Nominal": 1,
        "Name": "Румынский лей",
        "Value": 16.3718,
        "Previous": 16.3151,
    },
    "XDR": {
        "ID": "R01589",
        "NumCode": "960",
        "CharCode": "XDR",
        "Nominal": 1,
        "Name": "СДР (специальные права заимствования)",
        "Value": 100.6851,
        "Previous": 100.4475,
    },
    "SGD": {
        "ID": "R01625",
        "NumCode": "702",
        "CharCode": "SGD",
        "Nominal": 1,
        "Name": "Сингапурский доллар",
        "Value": 56.0117,
        "Previous": 56.0665,
    },
    "TJS": {
        "ID": "R01670",
        "NumCode": "972",
        "CharCode": "TJS",
        "Nominal": 10,
        "Name": "Таджикских сомони",
        "Value": 69.5841,
        "Previous": 69.5526,
    },
    "THB": {
        "ID": "R01675",
        "NumCode": "764",
        "CharCode": "THB",
        "Nominal": 10,
        "Name": "Таиландских батов",
        "Value": 21.6778,
        "Previous": 21.6542,
    },
    "TRY": {
        "ID": "R01700J",
        "NumCode": "949",
        "CharCode": "TRY",
        "Nominal": 10,
        "Name": "Турецких лир",
        "Value": 40.0816,
        "Previous": 40.0953,
    },
    "TMT": {
        "ID": "R01710A",
        "NumCode": "934",
        "CharCode": "TMT",
        "Nominal": 1,
        "Name": "Новый туркменский манат",
        "Value": 21.6973,
        "Previous": 21.6865,
    },
    "UZS": {
        "ID": "R01717",
        "NumCode": "860",
        "CharCode": "UZS",
        "Nominal": 10000,
        "Name": "Узбекских сумов",
        "Value": 66.5731,
        "Previous": 66.6691,
    },
    "UAH": {
        "ID": "R01720",
        "NumCode": "980",
        "CharCode": "UAH",
        "Nominal": 10,
        "Name": "Украинских гривен",
        "Value": 20.5624,
        "Previous": 20.552,
    },
    "CZK": {
        "ID": "R01760",
        "NumCode": "203",
        "CharCode": "CZK",
        "Nominal": 10,
        "Name": "Чешских крон",
        "Value": 33.9354,
        "Previous": 33.917,
    },
    "SEK": {
        "ID": "R01770",
        "NumCode": "752",
        "CharCode": "SEK",
        "Nominal": 10,
        "Name": "Шведских крон",
        "Value": 70.5394,
        "Previous": 70.973,
    },
    "CHF": {
        "ID": "R01775",
        "NumCode": "756",
        "CharCode": "CHF",
        "Nominal": 1,
        "Name": "Швейцарский франк",
        "Value": 81.6478,
        "Previous": 80.963,
    },
    "RSD": {
        "ID": "R01805F",
        "NumCode": "941",
        "CharCode": "RSD",
        "Nominal": 100,
        "Name": "Сербских динаров",
        "Value": 68.5543,
        "Previous": 68.3037,
    },
    "ZAR": {
        "ID": "R01810",
        "NumCode": "710",
        "CharCode": "ZAR",
        "Nominal": 10,
        "Name": "Южноафриканских рэндов",
        "Value": 41.1413,
        "Previous": 40.7495,
    },
    "KRW": {
        "ID": "R01815",
        "NumCode": "410",
        "CharCode": "KRW",
        "Nominal": 1000,
        "Name": "Вон Республики Корея",
        "Value": 57.3483,
        "Previous": 57.4064,
    },
    "JPY": {
        "ID": "R01820",
        "NumCode": "392",
        "CharCode": "JPY",
        "Nominal": 100,
        "Name": "Японских иен",
        "Value": 55.8757,
        "Previous": 55.3954,
    },
}


async def get_all_currencies():
    query = select(Currencies)
    return await Repository.all(query)


async def get_currency_by_char_code(char_code):
    query = select(Currencies).where(Currencies.char_code == char_code)
    return await Repository.scalar(query)


async def create_currency(currency: dict):
    query = insert(Currencies).values(**currency)
    await Repository.insert(query)


async def update_currencies_values(values):
    query = (
        update(Currencies)
        .where(Currencies.char_code == values["char_code"])
        .values(value=values["value"], updated_at=values["updated_at"])
    )
    await Repository.update(query)


async def update_or_create_currencies(currencies_json):
    for item in currencies_json.values():
        data = {
            "source_id": item["ID"],
            "char_code": item["CharCode"],
            "name": item["Name"],
            "value": item["Value"],
            "is_active": True,
            "updated_at": datetime.datetime.now(),
        }
        currency = await get_currency_by_char_code(item["CharCode"])
        if not currency:
            await create_currency(data)
        await update_currencies_values(data)


if __name__ == "__main__":
    asyncio.run(update_or_create_currencies(cur))
