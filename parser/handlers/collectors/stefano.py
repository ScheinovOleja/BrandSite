import asyncio
import random
import re

from aiohttp import ClientSession
from sqlalchemy.orm import Session

from parser.models import get_or_create, StefanoData


class ParserStefano:

    def __init__(self, url, session: Session):
        self.rate_sem = asyncio.BoundedSemaphore(20)
        self.url = url[0]
        self.category = url[1]
        self.session = session
        self.cookie = {
            "_iub_cs-60011850": "{\"timestamp\":\"2023-02-03T17:37:24.684Z\",\"version\":\"1.44.8\",\"purposes\":{\"1\":true,\"2\":true,\"3\":true,\"4\":true,\"5\":true},\"id\":\"60011850\",\"cons\":{\"rand\":\"c0a387\"}}",
            "ASP.NET_SessionId": "1gvbibqn0wfioc0yzowkut0j",
            "ROUTEID.63299f77bed394482cee1d79617241cd": ".node2",
            "SKYWALKER_SETTINGS": "BASE_PATH=it&NAZIONE=IT&LINGUA=ru&ALLOW_COOKIES=true",
            "SKYWALKER_SR_COOKIE": "true",
            "SKYWALKER_TRX": "GUID=8eab24e4-0eb4-4251-9edb-2fbf7b78069a&AFFILIAZIONE=&DATA_AFFILIAZIONE=00010101&SCADENZA_AFFILIAZIONE=00010101",
            "tc_cj_v2": "^cl_]ny[]]_mmZZZZZZKPQONNPNPOKOPZZZ]",
            "tc_cj_v2_cmp": "",
            "tc_cj_v2_med": "",
            "tCdebugLib": "1"
        }
        self.all_colors = [
            "T_157452",
            "T_161877",
            "T_157456",
            "T_157439",
            "T_157492",
            "T_167127",
            "T_157447",
            "T_157437",
            "T_157486",
            "T_157454",
        ]
        self.main_body = {
            "ParametroRicerca": {
                "Nome": "CAT",
                "Valore": "4AL"
            },
            "FiltriAggiuntivi": [
                {
                    "Nome": "CAT",
                    "Valore": "4AL"
                },
                {
                    "Nome": "DIST_COL",
                    "Valore": ""
                }
            ],
            "DimensionePagina": 1000,
            "PaginaCorrente": 0,
            "Ordinamento": "CAT_4AL"
        }
        self.all_products = []

    async def create_entry(self, article, title, subtitle, color, category, details, images):
        data = get_or_create(
            self.session,
            StefanoData,
            article=article,
            color=color,
            defaults={
                "title": title,
                "subtitle": subtitle,
                "details": details,
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
        async with ClientSession(cookies=self.cookie) as session:
            for color in self.all_colors:
                self.main_body['FiltriAggiuntivi'][1]['Valore'] = color
                async with session.post(
                        'https://www.stefanoricci.com/svc/ServizioInformazioniEsposizione.svc/Shop/Esposizione/OttieniInformazioniEsposizione',
                        json=self.main_body) as response:
                    data = await response.json()
                    self.all_products.extend(data['Value']['CodiciArticolo'])

    async def main(self):
        await self.get_all_products()
        rt = asyncio.create_task(self.releaser())
        await asyncio.gather(
            *[self.delay_wrapper(self.collect(product)) for product in self.all_products])
        rt.cancel()

    async def collect(self, sku):
        async with ClientSession(cookies=self.cookie) as session:
            async with session.get(
                    f"https://www.stefanoricci.com/svc/ServizioInformazioniProdotto.svc/Shop/Prodotti/OttieniInformazioniProdotto?codiceProdotto={sku}") as response:
                data = await response.json()
                article = data['Value']['CodiceProduttore'].split('.')[0]
                title = data['Value']['Descrizione']['Breve'].split(' цвет')[0]
                subtitle = '--'
                for color_item in data['Value']['Raggruppamento']['DistintiveTerziarie']:
                    if color_item['Nome']:
                        color = color_item['Descrizione']
                        break
                details = re.search(r"<ul>[\s\S]*</ul>", data['Value']['Scheda']).group(0)
                images = {'photos': []}
                images['photos'].extend([image['ImmagineHD'] for image in data['Value']['Immagini']])
                await self.create_entry(article, title, subtitle, color, self.category, details, images)
