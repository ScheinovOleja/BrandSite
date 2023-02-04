import asyncio

import pandas as pd
from aiohttp import ClientSession, TCPConnector
from flask import Blueprint, render_template
from sqlalchemy import text, select

from brand_site import db
from brand_site.utils.db.models import BrunelloData
from parser.handlers.general_funcs import create_b64_image

app = Blueprint('server_app', __name__)


@app.route("/", methods=["GET"])
async def main_page():
    data = [("Zilli", "zilli_data"),
            ("Loro Piana", "loropiana_data"),
            ("Dior", "dior_data"),
            ("Louis Vuitton", "louisvuitton_data"),
            ("Chanel", "chanel_data"),
            ("Brunello Cucinelli", "brunello_data"),
            ("Brioni", "brioni_data"),
            ("Stefano Ricci", "stefano_data"),
            ("Bottega Veneta", "bottega_data"),
            ("Celine", "celine_data"),
            ("Saint Laurent", "laurent_data"),
            ("Tom Ford", "ford_data")]
    return render_template("main_page.html", brands=data)


@app.route("/brand/<brand>", methods=["GET"])
async def choice_category(brand):
    with db.engine.connect() as conn:
        data = pd.read_sql_query(select(db.metadata.tables[brand].c.category).distinct(), conn).to_dict('list')
    return render_template("categories_page.html", data=data['category'], brand=brand)


@app.route("/brand/<brand>/category/<category>")
async def choice_item(brand, category):
    with db.engine.connect() as conn:
        data = pd.read_sql_query(select(db.metadata.tables[brand]).where(db.metadata.tables[brand].c.category == category), conn).to_dict('list')
    return render_template("item_page.html", data=data, brand=brand, category=category, count_records=len(data['id']))


async def get_photo_b64(photos):
    new_photos = []
    async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
        for i, photo_set in enumerate(photos):
            new_photos_set = []
            for photo in photo_set:
                image = await create_b64_image(session, photo)
                new_photos_set.append(image)
            new_photos.append(new_photos_set)
            await asyncio.sleep(0.01)
    return new_photos
