import asyncio
import json
import re

from aiohttp import ClientSession, TCPConnector
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from parser.handlers.general_funcs import BaseParser
from parser.models import get_or_create, BrandsData


class ParserDior(BaseParser):

    def __init__(self, url, session: Session):
        super(ParserDior, self).__init__(url, session)
        self.detail_url = "https://api-fashion.dior.com/graph?GetProductStocks="
        self.dior_url = 'https://www.dior.com'
        self.rate_sem = asyncio.BoundedSemaphore(10)
        self.main_body_bags = {
            "requests": [
                {
                    "query": "",
                    "indexName": "merch_prod_live_ru_ru",
                    "params": 'hitsPerPage=1000&restrictSearchableAttributes=["ean","sku"]&attributesToRetrieve=["color","style_ref","title", "products", "subtitle", "size", "products"]&filters=namespaces:women-allthebags OR namespaces:women-allthebags-2 OR namespaces:women-allthebags-3 OR namespaces:women-allthebags-4 AND type:"PRODUCT"&facets=["color.group",]'
                }
            ]
        }
        self.main_body_belts = {
            "requests": [
                {
                    "query": "",
                    "indexName": "merch_prod_live_ru_ru",
                    "params": 'hitsPerPage=1000&restrictSearchableAttributes=["ean","sku"]&attributesToRetrieve=["color","style_ref","title", "products", "subtitle", "size", "products"]&filters=namespaces:women-accessories-belts AND type:"PRODUCT"'
                }
            ]
        }
        self.second_body = {"operationName": "GetProductStocks",
                            "variables": {"id": ""},
                            "query": "query GetProductStocks($id: String!) {\n  product: getProduct(id: $id) {"
                                     "code,"
                                     "sizeAndFit,"
                                     "url,"
                                     "}}"
                            }
        self.main_headers = {
            "x-algolia-api-key": "64e489d5d73ec5bbc8ef0d7713096fba",
            "x-algolia-application-id": "KPGNQ6FJI9",
            "Host": "kpgnq6fji9-dsn.algolia.net",
            "Origin": "https://www.dior.com",
            "Referer": "https://www.dior.com/",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"
        }
        self.second_headers = {
            "Host": "api-fashion.dior.com",
            "apollographql-client-name": "Newlook Couture Catalog K8S",
            "apollographql-client-version": "5.247.1-8f13cb5e.hotfix",
            "x-dior-universe": "couture",
            "x-dior-locale": "ru_ru"
        }

    async def get_photos(self, url, code):
        async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
            async with session.get(self.dior_url + url) as response:
                extra_soup = BeautifulSoup(await response.text('utf-8'), "lxml")
                photos_raw = extra_soup.find_all('img', alt=re.compile('aria_openGallery'))
                if not photos_raw:
                    async with session.get(self.dior_url + f"/{code}") as response:
                        extra_soup = BeautifulSoup(await response.text('utf-8'), "lxml")
                        photos_raw = extra_soup.find_all('img', alt=re.compile('aria_openGallery'))
                images = {"photos": [link.attrs['src'] for link in photos_raw]}
        await asyncio.sleep(0.5)
        return images

    async def create_entry(self, article, title, subtitle, size_and_fit, colours, photos_links):
        data = get_or_create(
            self.session,
            BrandsData,
            article=article,
            title=title,
            defaults={
                "subtitle": subtitle,
                "size_and_fit": size_and_fit,
                "color": colours,
                "category": self.category,
                "images": photos_links,
                "brand": "dior"
            }
        )
        if data[1]:
            self.session.commit()
        await asyncio.sleep(0.5)

    async def get_all_products(self):
        async with ClientSession(headers=self.main_headers, connector=TCPConnector(verify_ssl=False)) as session:
            async with session.post(
                    self.url,
                    json=self.main_body_bags if self.category == 'bags' else self.main_body_belts) as response:
                main_json = json.loads(await response.text())
        self.all_products = main_json['results'][0]['hits']

    async def collect(self, product):
        try:
            article = f"{product['style_ref']}_{product['color']['code']}"
            self.second_body['variables']['id'] = article
            async with ClientSession(headers=self.second_headers, connector=TCPConnector(verify_ssl=False)) as session:
                async with session.post(self.detail_url, json=self.second_body) as response:
                    second_json = json.loads(await response.text())
                    product.update(second_json['data']['product'])
            await asyncio.sleep(0.1)
            title = product['title']
            subtitle = product['subtitle']
            try:
                size_and_fit = product['sizeAndFit'].replace('<br />', "\n")
                size_and_fit = size_and_fit.replace('Подробную информацию см. в размерной сетке.', '')
            except AttributeError:
                size_and_fit = '--'
            colours = product['color']['group']
            images = await self.get_photos(product['url'], product['code'])
            await self.create_entry(article, title, subtitle, size_and_fit, colours, images)
        except BaseException as e:
            print(f"Критическая ошибка -- пропуск ссылки -- сайт {self.url} \n {e}")
            return
