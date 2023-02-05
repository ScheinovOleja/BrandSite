import asyncio
import json
import random

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from parser.handlers.general_funcs import BaseParser
from parser.models import get_or_create, BrandsData


class ParserChanel(BaseParser):

    def __init__(self, url, session: Session):
        self.rate_sem = asyncio.BoundedSemaphore(5)
        super(ParserChanel, self).__init__(url, session)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
            "Accept": "application/json",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.chanel.com/ru/fashion/handbags/c/1x1x1x1/flap-bags/",
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
            "_abck": "345DAD8712F3BA5D9144B75AFAD0F8C8~0~YAAQZBdlX/DyU9GFAQAAb06RIAkQxuT9zY50FhbQ0AwTHX3FInHWAqiicarh6n9RtVIytfsvesg5rQ9o4XT3SwW7zzoEEnAGdTFBqDXmqZ8qtxXTKXrHIye0z95wPod9bllrqccbsXGtgTP7ycVl5EvN0B1etM+OSFOw76v2To1Q1sLn0jrXhXBUypaPHIvifUnEQJgvq8EDurzbfxEQqUoQeRx+PknA47c1jLkDAejVXlwTJTiOu+P79AvPJI4Ct7hkrmBOSpg+IT/KjzxOe2jeUbz6yefRILRlqs8xGiasuD9gu+zu9alrPl+BGY2yHyqkJ/G6p7p2c8FBQmIlsXIMmmIlHsJMeKFeLnol8xUupKYLO/4k7t+CLkvvHz37h2DVkwkR3SetclOtOm9Qu3AnCg+7VZvU~-1~-1~-1",
            "_gcl_au": "1.1.1179439699.1675354454",
            "ak_bmsc": "7343D95BE69843F012C423D0340CFAA4~000000000000000000000000000000~YAAQZBdlX0D0U9GFAQAAQruRIBKKXvip8h+s3q4Yg8c7jdFY9gDSLIvsYD8L2E/iPBz9iAcUQ7EESpo5h17jGSiY1BKddK+67BbkGfKBsYhjZ7R/zeEZDyjdHh8UNOwRhHP6OCi0CtsSTNPbtxYrEnALJR7oAyKr2wKJSUkuDkU0pCLqBqx7M3nEm+VWYQZzYs1AD/xrRGC6RvMDNfuvo5g2YZaRIGcIsI+yyVYqPR8cpTMlbGStE9r9TNap8e0uj+sZUGh39LCymUdYODCIsIImheJE4FhGOUuEUtQVi7vX6d78LTGTNuFkNZqqs3Nu3Ngvv9Z/NG5Tm4ke1OQXUQFiyPisJQ9q8ALJQ0Tm6ysMHUNwDYokIT5E7Uz5UT1QwDY8oZgwvNmHjQJmimNee0CwIQ0Vb+YXmwOKp7P1e4tHTbwiHpmDG/0AEtx17vRk+LsF07WvogWP",
            "AKA_A2": "A",
            "akacd_maintenance-ONE-EMEA-EU": "2177452799~rv=75~id=1d6d0ab88071ff26a6c3f3483d01b659",
            "akacd_maintenance-page-FSH-PRD": "2177452799~rv=26~id=3fc303e1a996efa6e1afcb01e103dea0",
            "AWSALB": "2q9eK1VQPVw++3qW4r+WT4EDMnWfZNF58MbECpzOrHd23QxBRpWznzFr07BuomOk4+En7Z3EvJJPy4zPjYfAFSGuvhjsqTXe35mn0vXUv1gGG+dn2wGldNAH6X0s",
            "AWSALBCORS": "2q9eK1VQPVw++3qW4r+WT4EDMnWfZNF58MbECpzOrHd23QxBRpWznzFr07BuomOk4+En7Z3EvJJPy4zPjYfAFSGuvhjsqTXe35mn0vXUv1gGG+dn2wGldNAH6X0s",
            "bm_mi": "37480DCCDAF807F9D5645FA860446410~YAAQZBdlX4LyU9GFAQAA2yORIBLEKMMrxVOYTCy37ephRtkEW2udY9reNGfb67PDozvjRkMU0ozEM6f4z5IlTDPHx03dOikw4z/RJ3q0XPFVsa5mrAqQJHhesvFiE4w8303qsOu1YoV6dsSuW4ZlEGeRDFem4iue1AyKgArcApllA7WKScqJkjYDQuYz/0KX9+3pjuyOzg1259pRBXRgepLeVJokDi/zah2hrRdCn6g7f8fIgohNBgfRZP6SWl0qc1qv3H9p5aFjbZepr2lngnFYv1iRB2xBDNm1oDbqU+z2eIKb2z67k8bfr0B8EeTOZZkqJWS5s+59ofoFgHjy20blIzJKJ6+c1o8=~1",
            "bm_sv": "D82762FE7D219290AA40E74449595626~YAAQZBdlX+7yU9GFAQAAvE2RIBLhJix7CAzSfeUi82AXyVxmuyLKxr61+LQaTZTGQcxc/136MAD/+TPIr1mqPLwXqDL+Xdcye8TWw9k4d+yR1HaaCYKlJ6VvPQEFKLJiVx0YWlZCbWxgdCc+UX7LO8kqU5RZg9vRARvzHjYMO95jRPOKJFKU4ia7Uh3HNHVXsH0J4VxnUZQLsBKDQLu7wTmPLvKDFIgEfPHPEeJWvs0HzdyUuK1bR6mpSUUm2NfaDg==~1",
            "bm_sz": "A574232CEF12CBF498B57E31C0DC80C0~YAAQPRdlX7WxIdyFAQAAI6qBIBIChiODScKR0XVlUFZ19281hiYfFrgS0Z7WnV/kIoB5xvL239KFqaWXMHiMBndT2IW+KTefjSP5t1pNgAlFttUTz6FXDn9rYR+lLtWohunp4T5n9KUycLIDs3bCQPlTMYrp1BJempRocIXYDelQOM6+XWiXgxzHIYzv6izhiZjDeZ8rMOBcR0/5NFfDEN2jQ6BBfw+a0ch58Are0HMxFil9Zl7xZkrBxvFuOHm4kzx8z/oaKQCHpH7sMwgiBQKmfPDY1vp8GZUmaXMIHWxGQEs=~3228978~3359299",
            "boutiqueApp": "false",
            "chanel_ru_ecom-cart": "e336cc94-355c-436d-9824-90dff373c9af",
            "country": "ME",
            "dtCookie": "v_4_srv_4_sn_0A2E3DA8E72AC8D1B89F8CAD741D6FF9_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_0",
            "isClient": "false",
            "JSESSIONID": "F917BCA2E2C8A7E2862E4807CCFA999D",
            "lang": "RU-ru_RU",
            "OptanonAlertBoxClosed": "2023-02-02T14:55:40.051Z",
            "OptanonConsent": "isGpcEnabled=0&datestamp=Sun+Feb+05+2023+09:23:15+GMT+0100+(Ð¦ÐµÐ½ÑÑÐ°Ð»ÑÐ½Ð°Ñ+ÐÐ²ÑÐ¾Ð¿Ð°,+ÑÑÐ°Ð½Ð´Ð°ÑÑÐ½Ð¾Ðµ+Ð²ÑÐµÐ¼Ñ)&version=6.36.0&isIABGlobal=false&hosts=&genVendors=&consentId=1b924c4b-79af-49e1-9e2b-b2572c3e90ef&interactionCount=1&landingPath=NotLandingPage&groups=1:1,2:1,3:1,4:1&geolocation=RU;EU&AwaitingReconsent=false",
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
            async with session.get(self.url) as response:
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
                images = {'photo': [image['url'] for image in item_data['basic']['images']]}
            except KeyError:
                return
            await self.create_entry(article, title, subtitle, color, self.category, size, images)
