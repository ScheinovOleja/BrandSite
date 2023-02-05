import pandas as pd
from flask import Blueprint, render_template
from sqlalchemy import select

from server import db
from utils.db.models import AllBrands, BrandsData

app = Blueprint('server_app', __name__)


@app.route("/", methods=["GET"])
async def main_page():
    with db.engine.connect() as con:
        data = pd.read_sql_query(
            select(AllBrands.name, AllBrands.short_name).join(BrandsData,
                                                              AllBrands.short_name == BrandsData.brand).distinct(),
            con).to_dict('list')
    return render_template("main_page.html", brand=data, count=len(data['name']))


@app.route("/<brand>", methods=["GET"])
async def choice_category(brand):
    with db.engine.connect() as conn:
        data = pd.read_sql_query(select(BrandsData.category).where(BrandsData.brand == brand).distinct(), conn).to_dict(
            'list')
    return render_template("categories_page.html", data=data['category'], brand=brand)


@app.route("/<brand>/<category>")
async def choice_item(brand, category):
    with db.engine.connect() as conn:
        data = pd.read_sql_query(
            select(BrandsData).where(BrandsData.brand == brand).filter(BrandsData.category == category), conn).to_dict(
            'list')
    return render_template("item_page.html", data=data, brand=brand, category=category, count_records=len(data['id']))
