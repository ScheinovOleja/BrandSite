import asyncio
import base64

from aiofiles import tempfile
from aiohttp import ClientSession, TCPConnector
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from webptools import base64str2webp_base64str, grant_permission


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
        await self.get_all_products()
        rt = asyncio.create_task(self.releaser())
        await asyncio.gather(
            *[self.delay_wrapper(self.collect(product)) for product in self.all_products])
        rt.cancel()

    async def collect(self, product):
        pass

    async def create_b64_image(self, session, photo):
        async with session.get(photo) as response:
            image_in_b64 = base64.b64encode(await response.content.read())
            async with tempfile.NamedTemporaryFile() as file:
                webp_in_b64 = base64str2webp_base64str(image_in_b64.decode(), image_type='jpg', option='-q 50',
                                                       temp_path=file.name)
                await asyncio.sleep(0.1)
                return webp_in_b64[0]

    async def get_photo_b64(self, photos):
        new_photos = []
        grant_permission()
        async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
            for i, photo_set in enumerate(photos):
                new_photos_set = []
                for photo in photo_set:
                    image = await self.create_b64_image(session, photo)
                    new_photos_set.append(image)
                new_photos.append(new_photos_set)
                await asyncio.sleep(0.01)
        return new_photos

    async def translator(self, text):
        async with ClientSession() as session:
            url = f"https://translate.google.com/m?sl=en&tl=ru&hl=en&q={text}"
            async with session.get(url) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
                result_container = soup.find("div", {"class": "result-container"})
                if result_container:
                    translated_text = result_container.text
                else:
                    print('Слишком много запросов. Мы заблокированы(')
                    translated_text = text
        await asyncio.sleep(0.5)
        return translated_text
