import asyncio

import pandas as pd
from aiohttp import ClientSession, TCPConnector
from flask import Blueprint, render_template
from sqlalchemy import text, select

from brand_site import db
from brand_site.utils.db.models import BrandsData

app = Blueprint('server_app', __name__)


@app.route("/", methods=["GET"])
async def main_page():
    with db.engine.connect() as con:
        data = pd.read_sql_query(select(BrandsData.brand).distinct(), con).to_dict('list')
    return render_template("main_page.html", brands=data)


@app.route("/<brand>", methods=["GET"])
async def choice_category(brand):
    with db.engine.connect() as conn:
        data = pd.read_sql_query(select(BrandsData.category).distinct(), conn).to_dict('list')
    return render_template("categories_page.html", data=data['category'], brand=brand)


@app.route("/<brand>/<category>")
async def choice_item(brand, category):
    with db.engine.connect() as conn:
        data = pd.read_sql_query(select(BrandsData).where(BrandsData.category == category), conn).to_dict('list')
    return render_template("item_page.html", data=data, brand=brand, category=category, count_records=len(data['id']))
