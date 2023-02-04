import asyncio
import random

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from parser.models import get_or_create, CelineData


class ParserCeline:

    def __init__(self, url, session: Session):
        self.rate_sem = asyncio.BoundedSemaphore(50)
        self.url = url[0]
        self.category = url[1]
        self.session = session
        self.all_products = []

    async def create_entry(self, article, title, subtitle, color, category, details, images):
        data = get_or_create(
            self.session,
            CelineData,
            article=article,
            title=title,
            defaults={
                "subtitle": subtitle,
                "details": details,
                "color": color,
                "category": category,
                "images": images
            }
        )
        if data[1]:
            self.session.commit()
        await asyncio.sleep(random.choice([1.5, 2]))

    async def delay_wrapper(self, task):
        await self.rate_sem.acquire()
        return await task

    async def releaser(self):
        while True:
            await asyncio.sleep(0.5)
            try:
                self.rate_sem.release()
            except ValueError:
                pass

    async def get_all_products(self):
        async with ClientSession() as session:
            async with session.get(self.url) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
        all_product = soup.select("li.o-listing-grid__item > div > a")
        self.all_products.extend([(f"https://www.celine.com{item.get('href')}", item.parent.get('data-id')) for item in all_product])

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
        title = soup.find('span', class_="o-product__title-truncate").text
        subtitle = '--'
        color = soup.find('span', class_="o-product__title-color").text
        details = soup.find('div', class_="o-product__description").text
        all_images = soup.select('li.m-thumb-carousel__item > button > img')
        images = {'photos': []}
        images['photos'].extend(
            [image.get('src').split('?')[0] if image.get('src') else image.parent.get('data-pswp-src') for image in all_images])
        await self.create_entry(article, title, subtitle, color, self.category, details, images)
