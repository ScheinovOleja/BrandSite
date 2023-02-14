import asyncio
import random

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from parser.handlers.general_funcs import BaseParser
from parser.models import get_or_create, BrandsData


class ParserVersace(BaseParser):

    def __init__(self, url, session: Session):
        super(ParserVersace, self).__init__(url, session)
        self.rate_sem = asyncio.BoundedSemaphore(10)
        self.headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html, */*; q=0.01",
            "Host": "www.versace.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br"
        }
        self.status = 404

    async def create_entry(self, article, title, subtitle, color, category, details, description, images):
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
                "images": images,
                "brand": "versace"
            }
        )
        if data[1]:
            self.session.commit()
        await asyncio.sleep(random.choice([1.5, 2]))

    async def get_all_products(self):
        async with ClientSession(headers=self.headers) as session:
            while self.status != 200:
                async with session.get(self.url) as response:
                    if response.status != 200:
                        await asyncio.sleep(5)
                        self.status = response.status
                        continue
                    self.status = response.status
                    soup = BeautifulSoup(await response.text(), 'lxml')
        self.all_products = [item.get('href') for item in
                             soup.select("article > div.product-image > div > a")]

    async def collect(self, url):
        async with ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
        title = soup.find('h1', class_="js-product-name").text
        article = soup.find('span', class_="js-product-number").text
        subtitle = ''
        color = soup.select_one("span.attribute-value:nth-child(3)").text if soup.select_one(
            "span.attribute-value:nth-child(3)") else ''
        details = soup.find('div', class_="product-details").get_text()
        description = soup.find('div', class_="product-description").get_text()
        images = {"photos": [f"https://www.versace.com{image.get('src')}" for image in
                             soup.select("div.pdp-gallery-item > img")]}
        await self.create_entry(article, title, subtitle, color, self.category, details, description, images)
