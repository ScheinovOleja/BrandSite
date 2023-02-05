import asyncio
import random
import re

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from parser.handlers.general_funcs import BaseParser
from parser.models import BrandsData, get_or_create


class ParserBottega(BaseParser):

    def __init__(self, url, session):
        super(ParserBottega, self).__init__(url, session)
        self.rate_sem = asyncio.BoundedSemaphore(100)

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
                "brand": "bottega"
            }
        )
        if data[1]:
            self.session.commit()
        await asyncio.sleep(random.choice([1.5, 2]))

    async def get_all_products(self):
        async with ClientSession() as session:
            async with session.get(self.url) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
        all_products = soup.find_all('a', class_='c-product__link')
        self.all_products.extend(
            [(f"https://www.bottegaveneta.com{link.get('href')}", link.get('data-pid')) for link in all_products])

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
        title = " ".join(soup.find('h1', class_="c-product__name").text.replace('\n\n', '').split())
        subtitle = '--'
        color = " ".join(soup.find('span', class_="l-pdp__colorname").text.replace('\n\n', '').split())
        details = re.sub(" +", " ", soup.find('div', class_="l-pdp__description").text.replace('\n\n', ''))
        all_image = soup.find_all("img", class_="c-product__image")
        images = {'photos': [image.get('src') for image in all_image]}
        await self.create_entry(article, title, subtitle, color, self.category, details, images)
