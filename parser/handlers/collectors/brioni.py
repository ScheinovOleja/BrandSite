import asyncio
import random

from aiohttp import ClientSession
from sqlalchemy.orm import Session

from parser.handlers.general_funcs import BaseParser
from parser.models import get_or_create, BrandsData


class ParserBrioni(BaseParser):

    def __init__(self, url, session: Session):
        super(ParserBrioni, self).__init__(url, session)
        self.headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "x-algolia-api-key": "4e36de8bb30642db2d0fdd7244874d3e",
            "x-algolia-application-id": "WNP6TQNC8R"
        }
        self.body = {
            "query": "",
            "page": 0,
            "hitsPerPage": 200,
            "filters": "hierarchicalCategories.lvl0.value:\"Верхняя одежда||category___outerwear\"",
            "facetFilters": []
        }

    async def create_entry(self, article, title, subtitle, color, category, materials, details, images):
        data = get_or_create(
            self.session,
            BrandsData,
            article=article,
            defaults={
                "title": title,
                "subtitle": subtitle,
                "materials": materials,
                "details": details,
                "color": color,
                "category": category,
                "images": images,
                "brand": "brioni"
            }
        )
        if data[1]:
            self.session.commit()
        await asyncio.sleep(random.choice([1.5, 2]))

    async def get_photos(self, article, mfc):
        photo_ids = []
        images = {'photos': []}
        async with ClientSession(
                headers={"Authorization": "Bearer vWpzVvwL58z3mWIdoxBvXti9q5zrD793BctKe-5Qx3o"}) as session:
            async with session.get(
                    f"https://cdn.contentful.com/spaces/w2dr5qwt1rrm/environments/master/entries?links_to_entry={article}&include=2&locale=ru") as response:
                data = await response.json()
                data_assets = data['includes']['Asset']
                materials = ''
                for entry in data['includes']['Entry']:
                    if entry['sys']['id'] == article:
                        for material in entry['fields']['materials']:
                            materials += f"{material['percentage']}% {material['type']}\n"
                for entry in data['includes']['Entry']:
                    if "wrapperImage" in entry['sys']['id']:
                        photo_ids.append(entry['fields']['title'])
                if not photo_ids:
                    for entry in data['includes']['Entry']:
                        if "image" in entry['fields'].keys():
                            photo_ids.append(entry['fields']['title'])
                for asset in data_assets:
                    images['photos'].extend([f"https:{asset['fields']['file']['url']}" for photo_id in photo_ids if
                                             asset['fields']['title'].replace('.jpg',
                                                                              '') == photo_id and mfc in photo_id])
        await asyncio.sleep(0.5)
        return images, materials

    async def get_all_products(self):
        async with ClientSession(headers=self.headers) as session:
            async with session.post(
                    "https://wnp6tqnc8r-3.algolianet.com/1/indexes/prod_primary_index_products_milan-noeu_ru/query",
                    json=self.body) as response:
                data = await response.json()
                data = data['hits']
                self.all_products.extend([item for item in data])

    async def collect(self, item):
        article = item['mfc']
        title = item['title']
        subtitle = '--'
        details = item['details']
        color = item['colors'][0]['label']
        images, materials = await self.get_photos(item['objectID'], item['mfc'])
        await self.create_entry(article, title, subtitle, color, self.category, materials, details, images)
