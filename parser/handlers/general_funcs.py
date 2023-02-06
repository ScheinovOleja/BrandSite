import asyncio

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session


class BaseParser:

    def __init__(self, url, session: Session):
        self.rate_sem = asyncio.BoundedSemaphore(100)
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

    async def get_all_products(self):
        pass

    async def main(self):
        try:
            await self.get_all_products()
        except asyncio.exceptions.TimeoutError:
            return
        rt = asyncio.create_task(self.releaser())
        await asyncio.gather(
            *[self.delay_wrapper(self.collect(product)) for product in self.all_products])
        rt.cancel()

    async def collect(self, product):
        pass
