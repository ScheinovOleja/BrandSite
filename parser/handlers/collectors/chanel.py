import asyncio
import json
import random

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from handlers.general_funcs import BaseParser
from models import get_or_create, BrandsData


class ParserChanel(BaseParser):

    def __init__(self, url, session: Session):
        self.rate_sem = asyncio.BoundedSemaphore(5)
        super(ParserChanel, self).__init__(url, session)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
            "Accept": "application/json",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers"
        }
        self.cookies = {
            "_abck": "345DAD8712F3BA5D9144B75AFAD0F8C8~0~YAAQZBdlX3S8aNGFAQAA/yQMJgmoyZLE1Nne25YVoC1O3oLIuXyoTrRaKOTfum5rLe9zdtJx4qz2mVi1k3MRFsb/AKvsQH8pSNZPpi3ZeBC8wUohOlpZerepjAu1OFeSQaoDWrW8qbuv9ysp/tTvDrq52l7CAzIsuEhEoRRj8f0RFDL6eA2Rb6LbQnCqJadZtJJa9xiLJKA04Py+FF71+ASLCTyJ4ETOkhCFmOuSzMDLwm7jPc2gIyQN7xJY1crPCY4UPLxrLmEA4hKXmRF5m4q7F/v0It7j6KTzlK3r1TkrcliU8CqWXMBNAsyp8kOHJ+g8V+VPKX6EXeJm8Q0Tb27P2qnSjGE6i2l6FsuYK9UaW1OFlHg7mcuUYU7Fgw6qdemeCtc8mBPpVQfxyYI35b8e0Nrb2lpc~-1~||-1||~-1",
            "_gcl_au": "1.1.1179439699.1675354454",
            "ak_bmsc": "985D850756A812EAE26C9DC4D1D6F812~000000000000000000000000000000~YAAQZBdlX1i8aNGFAQAANSEMJhJQEn/MridekmAzRhd49Lmr1WgMqJnN+YR93MV4hYL5EA2X3NWTPVr1meHybffytdfZoVj1hj/hlgQelT5/avAT0yvYW+47GOnvrZmusZshCm4vohQGfgDBAa8sxebTBjAkAb7Cd61HbpV3fhM1zTEo8Cgg/PHFiD5ThzG7EBNbVr88ejP/2jQkLPBefz7/0203QrleB7eUffk2BBxLn4lxq8wZ4sYh6XhGPhq1i+8IGmag6Q9tGZKN6cT913Io1FiU4QCHqiHNlDIDxgtg4NFvd1WEZi/WBXjlQe8NR582DrL6z+eGQRKos8Y5CiZCSiXEOFqQdRI7qlbGS7nEPH0urNERKvzHFDFGLzEUE1ggauw7i/c=",
            "AKA_A2": "A",
            "akacd_maintenance-ONE-EMEA-EU": "2177452799~rv=75~id=1d6d0ab88071ff26a6c3f3483d01b659",
            "akacd_maintenance-page-FSH-PRD": "2177452799~rv=26~id=3fc303e1a996efa6e1afcb01e103dea0",
            "AWSALB": "qRo6DmmXk6QFZPhaVQwnzs35m9nDncPZwSXNzRf5d/HNRcr2rQI0BB5HuJciIQ3NiMLmFj5Pym0ybiASPY5sPYbhkFrfuObc1DfKIzP4saPAsv4SQi7/7vsZbSQI",
            "AWSALBCORS": "qRo6DmmXk6QFZPhaVQwnzs35m9nDncPZwSXNzRf5d/HNRcr2rQI0BB5HuJciIQ3NiMLmFj5Pym0ybiASPY5sPYbhkFrfuObc1DfKIzP4saPAsv4SQi7/7vsZbSQI",
            "bm_mi": "7C8BE58AD0D83FFF1CDD8281C392F69B~YAAQZBdlX2PAaNGFAQAA8MkMJhLIe6Bn/hMFCZBaMiTJETQe1N6eVjj2pEYZmi5XGGDC1QGyjWVtlopFV6lYpiUKZhEHMHuexXPc5UJfwxKWmdDhBGUOON02856d2hVRa/KvfsJJf8JmJB+j0ngro7aVBdjV1Zl1AO3AGyW+q6N8WjScN9CwfWqZnWaNq1/aRStNxSi26qOfn/r9SuWX11avupyUAE6W+n5D49BFD9SprtNcFtST6EeRku/VxF8z9ZXDhKtkYRzKOOJnJxQq78+68dm3W9baRnff2ZMt+SDYT8Z3K7moJdL9ZMi96/GH3bhtpXQLEm3v1zakeQdJmtqpa7Manlmva8o=~1",
            "bm_sv": "180D243F2904FBA8FED009392ED24DCD~YAAQZBdlXzLBaNGFAQAAXO8MJhLqhr74YE1UxlHttcHKksFYAVc0gQJesrColl6CdCUeyqY9LfPVJ4om7+Z6YpkygHTPxTmJ/29jP8KpgTEwftEqPgXcTU/DSxe7KWcg/ZVCaGE/3WqCFc4Ei4YEVjghzxHwOOTInEsgKCN/dm5C6oXpxeDmz/FX0VD0MuSOnhoChmhljlAeNtQkLpS59Qa9UYTo/kY0PyiettSk1+DCtEqbjiVC6bGe26dF7+Fj/Q==~1",
            "bm_sz": "87123F3236602C3C4061AD636393BD3E~YAAQZBdlX1q8aNGFAQAANSEMJhJgOtmUOwzw1eLbrYDuxZAlLrJ3O9zzkKNxsjECCec0BJSYot81G2Jx2ITHa/afiL8pYQRGY7hWBdEkWrjgET8P+lI4fuASNmXAae+QuGqgDe/Ax3m05vAF/yEvSr0i8SFHfA2EManZWZqSD9ddlu5WYo0NHb1Qgi92mOit+MF6Br3NRyhUoLshW0WsGPtGL2yqE+CPbhxSKIWQkHvlR/0RCjrtfl5+l8fnC3PfQ8w/gFJ/h/a6LRKNellK/630TMmMgkIvoCQjDEzVO61uPFw=~3684148~3748929",
            "boutiqueApp": "false",
            "chanel_ru_ecom-cart": "e336cc94-355c-436d-9824-90dff373c9af",
            "country": "ME",
            "dtCookie": "v_4_srv_6_sn_800473C0152686A8A1D73E31BC26A223_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_0",
            "hp_lang": "ru",
            "isClient": "false",
            "JSESSIONID": "A7679FD24E2A64CBD98C44346FC1F7AF",
            "lang": "RU-ru_RU",
            "linkName": "Handbags",
            "OptanonAlertBoxClosed": "2023-02-02T14:55:40.051Z",
            "OptanonConsent": "isGpcEnabled=0&datestamp=Mon+Feb+06+2023+10:27:06+GMT+0100+(Ð¦ÐµÐ½ÑÑÐ°Ð»ÑÐ½Ð°Ñ+ÐÐ²ÑÐ¾Ð¿Ð°,+ÑÑÐ°Ð½Ð´Ð°ÑÑÐ½Ð¾Ðµ+Ð²ÑÐµÐ¼Ñ)&version=6.36.0&isIABGlobal=false&hosts=&genVendors=&consentId=1b924c4b-79af-49e1-9e2b-b2572c3e90ef&interactionCount=1&landingPath=NotLandingPage&groups=1:1,2:1,3:1,4:1&geolocation=RU;EU&AwaitingReconsent=false",
            "segment": "none"
        }

    async def create_entry(self, article, title, subtitle, color, category, size, images):
        data = get_or_create(
            self.session,
            BrandsData,
            article=article,
            title=title,
            defaults={
                "subtitle": subtitle,
                "size_and_fit": size,
                "color": color,
                "category": category,
                "images": images,
                "brand": "chanel"
            }
        )
        if data[1]:
            self.session.commit()
        await asyncio.sleep(random.choice([1.5, 2]))

    async def get_all_products(self):
        async with ClientSession(headers=self.headers, cookies=self.cookies) as session:
            async with session.get(self.url, timeout=10) as response:
                data = json.loads(await response.json())
                self.all_products.extend([item for item in data['elements']])
                await asyncio.sleep(random.randint(1, 3))

    async def collect(self, item):
        async with ClientSession(headers=self.headers, cookies=self.cookies) as session:
            async with session.get(
                    f"https://www.chanel.com/ru/yapi/product/{item['variants'][0]['code']}?"
                    "options=basic&site=chanel") as response:
                item_data = await response.json()
            await asyncio.sleep(random.randint(1, 3))
            article = item_data['reference']
            title = item['name']
            subtitle = item_data['fabric']['name']
            color = item_data['color']['name']
            try:
                await asyncio.sleep(random.randint(1, 3))
                async with session.get(f"https://www.chanel.com/ru/fashion/p/{item['code']}") as response:
                    soup = BeautifulSoup(await response.text(), "lxml")
                    size = soup.find("span", class_="js-dimension").text
            except BaseException:
                return
            try:
                images = {'photos': [image['url'] for image in item_data['basic']['images']]}
            except KeyError:
                return
            await self.create_entry(article, title, subtitle, color, self.category, size, images)
