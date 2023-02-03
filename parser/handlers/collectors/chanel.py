import asyncio
import json
import random

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from parser.models import get_or_create, ChanelData


class ParserChanel:

    def __init__(self, url, session: Session):
        self.rate_sem = asyncio.BoundedSemaphore(5)
        self.url = url[0]
        self.category = url[1]
        self.session = session
        self.headers = {
            "Host": "www.chanel.com",
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
            "_abck": "345DAD8712F3BA5D9144B75AFAD0F8C8~0~YAAQPRdlX2vw4NmFAQAAHeUVEwlM2jdB6aet4jD91SVgfNiu68Nw2GsdiY9Z6CnBtccmDIRBrAlMFGDUvuKZoqSbiMpI6jzdl8nhowu5CYh1WfSus9RVMElu2qh1+oXYEbI2k4AZHAF4C7Ejp7yOTs1HKRiuKa+AEfU9TJfYzii/Xyg9NOIJhTbcZL/2fq2ceBgRt8WUmIq2jmGpPs8r8rA5tFz8teFhuXIifch+yF781JwWmTQWJf3DiXp/J0pJustZJb+uZpWXrt6y7VLhAn113IqzpAk256nqlaa/hlDJzacKDD88W+LgSnMxTx5woeuGdgVS64KAxqTHOTVnRESM8r7WgznnyexiGUMD4jll5VRfUQN2IP3Xr1+tiRjFlCzLMkFRUMOJySFhJcCjQY2VY+6OR5Oo~-1~-1~-1",
            "_gcl_au": "1.1.1179439699.1675354454",
            "ak_bmsc": "57FF57511EB612D5238F34B17F4A6869~000000000000000000000000000000~YAAQPRdlX3jf4NmFAQAAzYQVExJt4BkyN2aMaUgYJ31CFqoherR3sA59d2GRFWwcEg7rX0dGe3v4NTAAe4lE9pVLVJikwDS8e6Pp4FpfP1bUAa45xfcy0LUR/pNwGsyz2wWERbLanf/marc/YhD4nRNWdA65IoslSxUeNssJXZ0yTaihU/1LdR71jabp5byVxjg80ciVHirSuJL2FXRH87+3ME4kJV4dfKX43w/h/g25e8WYJSLFHVg6evfyoiVpWP7DoN9jOYHV7PzdRYh4guCBZBx8OmwEpvpNtD13hxG33NKMUImgP1s2qqhII3N8fO1y5iENRTHKez+3p8u+fglfqLGdD2ps4wkfMfy9rVVHrTgaqJUNyUjQk3+R+eyr5QD+yHNnGA==",
            "AKA_A2": "A",
            "akacd_maintenance-ONE-EMEA-EU": "2177452799~rv=75~id=1d6d0ab88071ff26a6c3f3483d01b659",
            "akacd_maintenance-page-FSH-PRD": "2177452799~rv=26~id=3fc303e1a996efa6e1afcb01e103dea0",
            "AWSALB": "uz3vXkeGXPR2n9OieYOm9hUukrX5Ms7eNW5KtlJLnyjYwXDxa4jgYE0f/fG/2oY/xpfRbQdpeEwnwuSUtwx9DpamXqvwb126qATkHh25nfgfFh+pPaXw+oldgXTX",
            "AWSALBCORS": "uz3vXkeGXPR2n9OieYOm9hUukrX5Ms7eNW5KtlJLnyjYwXDxa4jgYE0f/fG/2oY/xpfRbQdpeEwnwuSUtwx9DpamXqvwb126qATkHh25nfgfFh+pPaXw+oldgXTX",
            "bm_mi": "D16CFFA9AD696EA0E5C844DC9BF34FA5~YAAQPRdlXzbm4NmFAQAAHq4VExLZnpdABuv3T7Jnn5OMx3IR045kuZz6K3SZxR334dncT+9Tas6+ZQis/WHk4kkrV273n92Yyw3B9JDNMSzHorjFFidEGHiajIP6iHz61Yu8GrCmAiXwh7ZY2L6VdupVh+vyy9hn50GzDbch34mt5hb1fSp9eNSPdkXdC6XqeP9O9NsjQAcwElK2efUU9U68/eK/+QCn8qDUqiYgyIzE2R6mnrC70eVPBwxg33yO/gZGw4uPa5YHpzwrW+MjFIc0ISAMu/oJd/HDYAilGI2v3j1yNIC9nApjtMATv475dg==~1",
            "bm_sv": "1040FA1E73106729FF41B79D26827BF6~YAAQPRdlX4fw4NmFAQAACuYVExLZdMckmmj/73zO+gbi9DTchd47lEktqGWLnfXu/6rqEMXL38LXiM+6gwVGhN/Rd0fgz1oj6cD0V4e2ZDRhK8/8AyLKOlb5r84KWYiBB+pl+0xxovqd9iPqv8GYNUb374b0/ZPd9NgmaP06zc/eWqe9o+YhJdHbh4eyw43agn21J40M0u/ZwjShaMWhPqBiZjC8BhZpLOHW1y1z53PjM4JAOKwLrYvdRjycauyG~1",
            "bm_sz": "3258CB3D3BAE0B50A1BD342464043ED0~YAAQPRdlX8Iby9mFAQAAoTugEhIUVrVkXwC8M8qHrisjZmTNVFBM7B5f8i7qMfH4wuiR3bP/k2Ybr2xDwKT9Y7Pgy3dA4mtFf+Rsen1qq6n6PqNxgDPxBkdvrSpKBC8RStXapwRydm3YmZbqZTrlwCTqlYYzl5FXkBm7Vdfr3HRS24yzo777H6kc+I2XDplYKhNZyuTlG6EPakCqsr04JG2aRW8rkl9o8rbpRNKS3GpMjyNNmhq0VCh5mitXTpXfSDOLVgCn/OPlcGwljAAYkoEvT+pwPizWQ7bGd0SEe8tFil4=~3552822~4343092",
            "boutiqueApp": "false",
            "chanel_ru_ecom-cart": "e336cc94-355c-436d-9824-90dff373c9af",
            "country": "ME",
            "dtCookie": "v_4_srv_7_sn_61E6D5A97E2FFE769325E3353A7EBB3C_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_0",
            "isClient": "false",
            "JSESSIONID": "0A5D4D1D4F975F1CF802BCD071085319",
            "lang": "RU-ru_RU",
            "linkName": "Handbags",
            "OptanonAlertBoxClosed": "2023-02-02T14:55:40.051Z",
            "OptanonConsent": "isGpcEnabled=0&datestamp=Thu+Feb+02+2023+18:04:06+GMT+0100+(Ð¦ÐµÐ½ÑÑÐ°Ð»ÑÐ½Ð°Ñ+ÐÐ²ÑÐ¾Ð¿Ð°,+ÑÑÐ°Ð½Ð´Ð°ÑÑÐ½Ð¾Ðµ+Ð²ÑÐµÐ¼Ñ)&version=6.36.0&isIABGlobal=false&hosts=&genVendors=&consentId=1b924c4b-79af-49e1-9e2b-b2572c3e90ef&interactionCount=1&landingPath=NotLandingPage&groups=1:1,2:1,3:1,4:1&geolocation=RU;EU&AwaitingReconsent=false",
            "segment": "none"
        }
        self.all_products = []

    async def create_entry(self, article, title, subtitle, color, category, size, images):
        data = get_or_create(
            self.session,
            ChanelData,
            article=article,
            title=title,
            defaults={
                "subtitle": subtitle,
                "size": size,
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
        async with ClientSession(headers=self.headers, cookies=self.cookies) as session:
            async with session.get(self.url) as response:
                data = json.loads(await response.json())
                self.all_products.extend([item for item in data['elements']])
                await asyncio.sleep(random.randint(1, 3))

    async def main(self):
        await self.get_all_products()
        rt = asyncio.create_task(self.releaser())
        await asyncio.gather(
            *[self.delay_wrapper(self.collect(product)) for product in self.all_products])
        rt.cancel()

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
            except BaseException as e:
                return
            images = {"photo": []}
            try:
                images['photo'].extend([image['url'] for image in item_data['basic']['images']])
            except KeyError:
                return
            await self.create_entry(article, title, subtitle, color, self.category, size, images)
