from aiohttp import ClientSession
from bs4 import BeautifulSoup


async def get_vpv_calendar_image_link():
    async with ClientSession() as session:
        url = "https://vpv.ru/calendar"
        async with session.get(url) as response:
            page_data = await response.text()
            soup = BeautifulSoup(page_data, 'html.parser')
            links = soup.find_all('div', {'class': 'fwpl-item el-viregoj'})
            img_link = links[0].contents[0].attrs['href']
    return img_link