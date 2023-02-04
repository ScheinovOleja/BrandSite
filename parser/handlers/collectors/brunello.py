import asyncio
import random

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from parser.handlers.general_funcs import BaseParser
from parser.models import get_or_create, BrandsData


class ParserBrunello(BaseParser):

    def __init__(self, url, session: Session):
        super(ParserBrunello, self).__init__(url, session)
        self.rate_sem = asyncio.BoundedSemaphore(50)

    async def create_entry(self, article, title, subtitle, color, category, details, images):
        data = get_or_create(
            self.session,
            BrandsData,
            article=article,
            defaults={
                "title": title,
                "subtitle": subtitle,
                "details": details,
                "color": color,
                "category": category,
                "images": images,
                "brand": "brunello"
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
