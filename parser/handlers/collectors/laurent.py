import asyncio
import random
import re

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from handlers.general_funcs import BaseParser
from models import get_or_create, BrandsData


class ParserLaurent(BaseParser):

    def __init__(self, url, session: Session):
        super(ParserLaurent, self).__init__(url, session)
        self.rate_sem = asyncio.BoundedSemaphore(50)

    async def create_entry(self, article, title, subtitle, color, category, details, images):
        data = get_or_create(
            self.session,
            BrandsData,
            article=article,
            title=title,
            defaults={
                "subtitle": subtitle,
                "details": details,
                "color": color,
                "category": category,
                "images": images,
                "brand": "laurent"
            }
        )
        if data[1]:
            self.session.commit()
        await asyncio.sleep(random.choice([1.5, 2]))

    async def get_all_products(self):
        async with ClientSession() as session:
            async with session.get(self.url) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
        all_product = soup.find_all('a', class_="c-product__link")
        self.all_products.extend(
            [(f"https://www.ysl.com{link.get('href')}", link.parent.get('id')) for link in all_product])

    async def main(self):
        await self.get_all_products()
        rt = asyncio.create_task(self.releaser())
        await asyncio.gather(
            *[self.delay_wrapper(self.collect(product[0], product[1])) for product in self.all_products])
        rt.cancel()

    async def collect(self, url, article):
        async with ClientSession() as session:
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
        title = re.sub(" +", " ", soup.find('h1', class_="c-product__name").text)
        subtitle = '--'
        details = re.sub(" +", " ", soup.find('ul', class_="c-product__detailslist").text.replace('\n\n', ''))
        color = re.sub(" +", " ", soup.find('p', class_="c-product__colorvalue").text)
        all_image = soup.find_all('img', class_="c-product__image")
        images = {'photos': [image.get('src') for image in all_image]}
        await self.create_entry(article, title, subtitle, color, self.category, details, images)
