import asyncio
import random
import re

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from parser.models import get_or_create, FordData


class ParserFord:

    def __init__(self, url, session: Session):
        self.rate_sem = asyncio.BoundedSemaphore(50)
        self.url = url[0]
        self.category = url[1]
        self.session = session
        self.all_products = []
        self.start = 0
        self.size = 60

    async def create_entry(self, article, title, subtitle, color, category, details, images):
        data = get_or_create(
            self.session,
            FordData,
            article=article,
            color=color,
            defaults={
                "title": title,
                "subtitle": subtitle,
                "details": details,
                "category": category,
                "images": images
            }
        )
        if data[1]:
            self.session.commit()
        await asyncio.sleep(random.choice([1.5, 2]))

    async def get_all_products(self):
        async with ClientSession() as session:
            while self.start <= self.size:
                async with session.get(self.url.format(start=self.start, size=self.size)) as response:
                    soup = BeautifulSoup(await response.text(), 'lxml')
                all_product = soup.find_all('a', class_="overlay-link")
                self.all_products.extend(
                    [(link.get('href'), link.parent.get('data-itemsku')) for link in all_product])
                self.start += self.size

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
        title = re.sub(" +", " ", soup.find('h1', class_="product-name").text)
        subtitle = '--'
        details = re.sub(" +", " ", soup.select_one("#collapseTwo > div").text.replace('\n\n', ''))
        color = re.sub(" +", " ", soup.find('span', class_="selected-value").text)
        all_image = soup.find_all('img', class_="primary-image")
        images = {'photos': []}
        images['photos'].extend(
            [image.get('src').split("?")[0] if not "data:image" in image.get('src') else
             image.get('data-src').split("?")[0] for image in
             all_image])
        await self.create_entry(article, title, subtitle, color, self.category, details, images)
