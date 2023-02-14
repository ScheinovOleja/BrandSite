import asyncio
import random
import re

from aiohttp import ClientSession, ContentTypeError
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from handlers.general_funcs import BaseParser
from models import get_or_create, BrandsData


class ParserZimmermann(BaseParser):

    def __init__(self, url, session: Session):
        super(ParserZimmermann, self).__init__(url, session)
        self.all_products = []
        self.rate_sem = asyncio.BoundedSemaphore(5)
        self.start = 1
        self.status = True

    async def create_entry(self, article, title, subtitle, color, category, details, description, materials, images):
        data = get_or_create(
            self.session,
            BrandsData,
            article=article,
            defaults={
                "title": title,
                "subtitle": subtitle,
                "details": details,
                "category": category,
                "color": color,
                "description": description,
                "materials": materials,
                "images": images,
                "brand": "zimmermann"
            }
        )
        if data[1]:
            self.session.commit()
        await asyncio.sleep(random.choice([1.5, 2]))

    async def get_all_products(self):
        async with ClientSession() as session:
            while self.status:
                async with session.get(self.url.format(self.start)) as response:
                    try:
                        data = BeautifulSoup(getattr(await response.json(), 'categoryProducts'), "lxml")
                    except (ContentTypeError, AttributeError):
                        data = BeautifulSoup(await response.text(), 'lxml')
                if data.find('div', class_="empty"):
                    break
                self.all_products.extend(
                    [[item.get('href'), item.get('data-id')] for item in data.select("li.product-item > div > a")])
                self.start += 1

    async def main(self):
        try:
            await self.get_all_products()
        except asyncio.exceptions.TimeoutError:
            return
        rt = asyncio.create_task(self.releaser())
        await asyncio.gather(
            *[self.delay_wrapper(self.collect(product[0], product[1])) for product in self.all_products])
        rt.cancel()

    async def collect(self, product, article):
        async with ClientSession() as session:
            async with session.get(product) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
        title = soup.find("div", class_="product-view__main-details").find("h1").find("span").text.strip()
        subtitle = ''
        try:
            color = soup.select_one("div.product-view__color-variant-item > h5").text.strip()
        except AttributeError:
            color = ''
        materials_elem = soup.select_one("div.product-view__sizecare-care > span")
        materials = re.sub("<span>|<br/>|</span>", '',
                           materials_elem.prettify().partition("<br/>\n <br/>\n")[0]).replace('\n \n', '\n')
        details_elem = soup.find("div", class_="product-view__styling-webnote").find("span").find("ul")
        details = "\n".join([item for item in details_elem.strings])
        description = details_elem.parent.prettify().partition('<br/>')[0].replace("<span>", '')
        images = {"photos": [image.get('data-original') for image in soup.select(
            "li.js-product-gallery__slider-image > div.product-gallery__slider-product > img")]}
        await self.create_entry(article, title, subtitle, color, self.category, details, description, materials, images)
