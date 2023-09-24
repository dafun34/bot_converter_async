from aiohttp import ClientSession

WEATHER_PARAMS = {"format": 3, "lang": "ru"}

#
# def get_weather_by_city(city):
#     """Получить погоду по городу."""
#     async with ClientSession as session:
#         async with session.get()
#     url = f"https://wttr.in/{city}?0"
#     weather = requests.get(url, WEATHER_PARAMS).text
#     return weather
