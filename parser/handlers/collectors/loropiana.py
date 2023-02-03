import asyncio
import random

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from fake_headers import Headers
from sqlalchemy.orm import Session

from parser.models import LoropianaData, get_or_create


class ParserLoropiana:

    def __init__(self, url, session: Session):
        self.rate_sem = asyncio.BoundedSemaphore(2)
        self.url = url[0]
        self.category = url[1]
        self.session = session
        self.product_list = []
        self.page = 0
        self.max_page = 999
        self.headers = Headers(
            browser="firefox",
            os="lin",
            headers=True
        )
        self.all_products = []

    async def create_entry(self, article, title, subtitle, color, category, details, images):
        data = get_or_create(
            self.session,
            LoropianaData,
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
        async with ClientSession(headers=self.headers.generate()) as session:
            while self.page <= self.max_page:
                async with session.get(self.url.format(self.page)) as response:
                    items = await response.json()
                    self.all_products.extend(items['results'])
                    self.max_page = items['pagination']['numberOfPages']
                    self.page += 1
                    await asyncio.sleep(random.choice([1.5, 2]))

    async def main(self):
        await self.get_all_products()
        rt = asyncio.create_task(self.releaser())
        await asyncio.gather(
            *[self.delay_wrapper(self.collect(product)) for product in self.all_products])
        rt.cancel()

    async def collect(self, item):
        async with ClientSession(headers=self.headers.generate()) as session:
            await asyncio.sleep(random.choice([1.5, 2]))
            async with session.get(f"https://ua.loropiana.com/ru/api/pdp/product-variants?articleCode="
                                   f"{item['code'].split('_')[0]}&colorCode={item['code'].split('_')[1]}") as response:
                item_detail = await response.json()
                item_detail = item_detail[0]
            await asyncio.sleep(random.choice([1.5, 2]))
            article = item['code']
            title = item['name']
            subtitle = item['eshopMaterialCode']
            color = item_detail['description']
            async with session.get(f"https://ua.loropiana.com/ru{item['url']}") as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
                await asyncio.sleep(random.choice([1.5, 2]))
            details = soup.select_one('div#productDetail > div.content > p.t-product-copy').text.replace(
                'Product sheet for environmental qualities or characteristics', '')
            images = {'photo': []}
            for image_item in item_detail['imagesContainers']:
                images["photo"].extend([image['url'] for image in image_item['formats'] if
                                        image_item['code'] != 'B1' and image['format'] == 'LARGE'])
            await self.create_entry(article, title, subtitle, color, self.category, details, images)
