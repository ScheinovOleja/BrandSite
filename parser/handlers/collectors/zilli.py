import asyncio
import re

from aiohttp import ClientSession, TCPConnector
from bs4 import BeautifulSoup, Tag, NavigableString
from sqlalchemy.orm import Session

from parser.handlers.general_funcs import BaseParser
from parser.models import BrandsData, get_or_create


class ParserZilli(BaseParser):

    def __init__(self, url, session: Session):
        super(ParserZilli, self).__init__(url, session)
        self.rate_sem = asyncio.BoundedSemaphore(30)
        self.more_detail_raw = []

    async def create_entry(self, article, title, subtitle, more_detail, materials, photos):
        data = get_or_create(
            self.session,
            BrandsData,
            article=article,
            title=title,
            defaults={
                "subtitle": subtitle,
                "details": more_detail,
                "materials": materials,
                "category": self.category,
                "images": photos,
                "brand": "zilli"
            }
        )
        if data[1]:
            self.session.commit()
        await asyncio.sleep(0.5)

    async def get_title(self, soup):
        try:
            title = soup.find('h1', class_='main-title').text
        except BaseException:
            title = "--"
        await asyncio.sleep(0.5)
        return title

    async def get_subtitle(self, soup):
        try:
            subtitle = soup.find('div', id='product-description-short')
            subtitle = [item for item in subtitle.children if not isinstance(item, NavigableString)][0].text
        except BaseException:
            subtitle = '--'
        await asyncio.sleep(0.5)
        return subtitle

    async def get_more_detail(self, soup):
        try:
            self.more_detail_raw = soup.select_one('.product_infos_tabs > li:nth-child(1) > div:nth-child(2) > '
                                                   'ul:nth-child(1)')
            if self.more_detail_raw:
                more_detail = "\n".join(
                    [li_text.text for li_text in self.more_detail_raw.contents[:-2] if not isinstance(li_text,
                                                                                                      NavigableString)])
            else:
                more_detail = soup.select_one('.product_infos_tabs > li:nth-child(1) > div:nth-child(2) > '
                                              'ul:nth-child(1)').text
        except BaseException:
            more_detail = "--"
        await asyncio.sleep(0.5)
        return more_detail

    async def get_materials(self, soup):
        try:
            materials_raw = soup.select_one('.product_infos_tabs > li:nth-child(2) > div:nth-child(2) > '
                                            'ul:nth-child(1)')
            if materials_raw:
                materials = "\n".join(
                    [li_text.text for li_text in materials_raw.contents if
                     not isinstance(li_text, NavigableString)])
            else:
                materials = soup.select_one('.product_infos_tabs > li:nth-child(2) > div:nth-child(2) > '
                                            'p:nth-child(1)').text
        except BaseException:
            materials = '--'
        await asyncio.sleep(0.5)
        return materials

    async def get_article(self, soup):
        try:
            article = soup.find('li', string=[re.compile(r"Ref. *"), re.compile(r"Réf. *"), re.compile(
                r"[A-Z0-9]{3,}-[A-Z0-9]{3,}-[A-Z0-9]{3,}/[A-Z0-9]{3,} [A-Z0-9]*")]).text
        except BaseException:
            if isinstance(self.more_detail_raw[-2], Tag) and len(self.more_detail_raw) > 2:
                article = self.more_detail_raw[-2].text
            elif isinstance(self.more_detail_raw[-2], Tag) and len(self.more_detail_raw) <= 2:
                article = re.search(r"[A-Z0-9]{3,}-[A-Z0-9]{3,}-[A-Z0-9]{3,}/[A-Z0-9]{3,} [A-Z0-9]*",
                                    self.more_detail_raw[-2].text).group(0)
            else:
                article = self.more_detail_raw[-1].text
        await asyncio.sleep(0.5)
        return article

    async def get_all_products(self):
        async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
            async with session.get(self.url) as main_response:
                main_soup = BeautifulSoup(await main_response.text(), "lxml")
                self.all_products = main_soup.find_all('a', class_="product-thumbnail")
        return self.all_products

    async def collect(self, link):
        try:
            async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
                async with session.get(link.attrs['href']) as response:
                    soup = BeautifulSoup(await response.text(), 'lxml')
            await asyncio.sleep(0.5)
            title = await self.get_title(soup)
            subtitle = await self.get_subtitle(soup)
            more_detail = await self.get_more_detail(soup)
            materials = await self.get_materials(soup)
            article = await self.get_article(soup)
            images = {
                'photos': [link.attrs['src'] for link in soup.find_all('img', {'itemprop': "image"})]}
            await self.create_entry(article, title, subtitle, more_detail, materials, images)
        except BaseException as e:
            print(f"Критическая ошибка -- пропуск ссылки -- сайт {self.url} - {e}")
            return
