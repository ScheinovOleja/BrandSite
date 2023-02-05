import asyncio
import random

from aiohttp import ClientSession
from bs4 import BeautifulSoup, Tag
from sqlalchemy.orm import Session

from handlers.general_funcs import BaseParser
from models import get_or_create, BrandsData


class ParserCeline(BaseParser):

    def __init__(self, url, session: Session):
        self.rate_sem = asyncio.BoundedSemaphore(1)
        super(ParserCeline, self).__init__(url, session)

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
                "brand": "celine"
            }
        )
        if data[1]:
            self.session.commit()
        await asyncio.sleep(random.choice([1.5, 2]))

    async def get_all_products(self):
        async with ClientSession() as session:
            async with session.get(self.url) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
        all_product = soup.select("li.o-listing-grid__item > div > a")
        self.all_products.extend(
            [(f"https://www.celine.com{item.get('href')}", item.parent.get('data-id')) for item in all_product])

    async def main(self):
        await self.get_all_products()
        rt = asyncio.create_task(self.releaser())
        await asyncio.gather(
            *[self.delay_wrapper(self.collect(product[0], product[1])) for product in self.all_products])
        rt.cancel()

    async def collect(self, url, article):
        ok = False
        async with ClientSession() as session:
            while not ok:
                async with session.get(url) as response:
                    soup = BeautifulSoup(await response.text(), 'lxml')
                    ok = response.ok
                    print(ok)
        title = soup.find('span', class_="o-product__title-truncate").text
        subtitle = '--'
        color = soup.find('span', class_="o-product__title-color").text
        try:
            details = "\n".join(
                [item.text for item in soup.select_one("div.o-product__description > div > p").contents if
                 not isinstance(item, Tag)])
        except AttributeError as e:
            details = "\n".join(
                [item.text for item in soup.select_one(
                    "div.a-list:nth-child(2) > div > p").contents if
                 not isinstance(item, Tag)])
            print(url)
        all_images = soup.select('li.m-thumb-carousel__item > button > img')
        images = {
            'photos': [image.get('src').split('?')[0] if image.get('src') else image.parent.get('data-pswp-src') for
                       image in all_images]}
        await self.create_entry(article, title, subtitle, color, self.category, details, images)
