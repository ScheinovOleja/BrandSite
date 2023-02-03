import asyncio
import random

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from parser.models import get_or_create, BrunelloData


class ParserBrunello:

    def __init__(self, url, session: Session):
        self.rate_sem = asyncio.BoundedSemaphore(50)
        self.url = url[0]
        self.category = url[1]
        self.session = session
        self.all_products = []

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

    async def create_entry(self, article, title, subtitle, color, category, details, images):
        data = get_or_create(
            self.session,
            BrunelloData,
            article=article,
            defaults={
                "title": title,
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

    async def get_all_products(self):
        async with ClientSession() as session:
            async with session.get(self.url) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
                all_links = soup.select("div.product-grid > div.col-sm-4 > div.product")
                self.all_products.extend([url.get('data-pid') for url in all_links])

    async def main(self):
        await self.get_all_products()
        rt = asyncio.create_task(self.releaser())
        await asyncio.gather(
            *[self.delay_wrapper(self.collect(product)) for product in self.all_products])
        rt.cancel()

    async def collect_variant(self, article):
        async with ClientSession() as session:
            async with session.get(
                    f"https://shop.brunellocucinelli.com/on/demandware.store/Sites-bc-ru-Site/ru_RU/Product-Variation?"
                    f"pid={article}") as response:
                item = await response.json()
                item = item['product']
                title = item['productName']
                subtitle = item['materials']
                color = item['mainColor']
                details = item['details']
                images = {'photos': []}
                images['photos'].extend([image['absURL'] for image in item['images']['large']])
                await self.create_entry(article, title, subtitle, color, self.category, details, images)

    async def collect(self, article):
        async with ClientSession() as session:
            async with session.get(
                    f"https://shop.brunellocucinelli.com/on/demandware.store/Sites-bc-ru-Site/ru_RU/Product-Variation?"
                    f"pid={article}") as response:
                data = await response.json()
                data = data['product']
            if len(data['variationAttributes'][0]['values']) > 1:
                for item in data['variationAttributes'][0]['values']:
                    await self.collect_variant(data['id']+item['id'])
            else:
                await self.collect_variant(data['sku'])

