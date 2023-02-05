import asyncio
import random
import re

from aiohttp import ClientSession
from sqlalchemy.orm import Session

from handlers.general_funcs import BaseParser
from models import get_or_create, BrandsData


class ParserLouis(BaseParser):
    def __init__(self, url, session: Session):
        super(ParserLouis, self).__init__(url, session)
        self.rate_sem = asyncio.BoundedSemaphore(50)
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Host": "api.louisvuitton.com",
            "TE": "trailers",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0"
        }
        self.page = 0
        self.max_page = 999

    async def create_entry(self, article, title, subtitle, color, category, description, images):
        data = get_or_create(
            self.session,
            BrandsData,
            article=article,
            title=title,
            defaults={
                "subtitle": subtitle,
                "description": description,
                "color": color,
                "category": category,
                "images": images,
                "brand": "louis"
            }
        )
        if data[1]:
            self.session.commit()
        await asyncio.sleep(random.choice([1.5, 2]))

    async def get_all_products(self):
        async with ClientSession(headers=self.headers) as session:
            while self.page <= self.max_page:
                async with session.get(self.url.format(self.page)) as response:
                    items = await response.json()
                    try:
                        self.all_products.extend(items['hits'])
                        self.max_page = items['nbPages']
                        self.page += 1
                        await asyncio.sleep(random.choice([1.5, 2]))
                    except KeyError:
                        return

    async def collect(self, item):
        async with ClientSession(headers=self.headers) as session:
            async with session.get(
                    f"https://api.louisvuitton.com/api/rus-ru/catalog/product/{item['productId']}") as response:
                total_data = await response.json()
        try:
            for model in total_data['model']:
                article = f"{item['productId']}-{item['identifier']}"
                title = item['name']
                subtitle = total_data['material']
                color = model['color']
                description = [description['value'] for description in model['additionalProperty'] if
                               description['name'] == 'detailedDescription']
                try:
                    description = re.sub(r"<p>\D*</p>|<li>|</li>|<ul>|</ul>", '\n', description[0])
                    description = re.sub(r"\n\n", '', description)
                except BaseException:
                    description = '--'
                images = {'photos':
                              [image['contentUrl'].format(IMG_WIDTH=1280, IMG_HEIGHT=720) for image in model['image']]}
                await self.create_entry(article, title, subtitle, color, self.category, description, images)
        except KeyError:
            return
