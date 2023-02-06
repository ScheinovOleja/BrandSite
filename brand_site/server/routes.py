import pandas as pd
from flask import Blueprint, render_template
from langdetect import LangDetectException
from server import db
from sqlalchemy import select
from utils.db.models import AllBrands, BrandsData

from brand_site.server.funcs import translator

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
    return render_template("items_page.html", data=data, brand=brand, category=category, count_records=len(data['id']))


@app.route("/<brand>/<category>/<article>")
async def item_detail(brand, category, article):
    from langdetect import detect
    with db.engine.connect() as conn:
        data = pd.read_sql_query(
            select(BrandsData).where(BrandsData.article == article).filter(
                BrandsData.category == category and BrandsData.brand == brand), conn
        ).to_dict('list')
    for i in range(len(data['id'])):
        try:
            if detect(data["subtitle"][i]) == "en":
                data["subtitle"][i] = await translator(data["subtitle"][i])
        except LangDetectException:
            pass
        try:
            if detect(data["materials"][i]) == "en":
                data["materials"][i] = await translator(data["materials"][i])
        except LangDetectException:
            pass
        try:
            if detect(data["details"][i]) == "en":
                data["details"][i] = await translator(data["details"][i])
        except LangDetectException:
            pass
        try:
            if detect(data["color"][i]) == "en":
                data["color"][i] = await translator(data["color"][i])
        except LangDetectException:
            pass
        try:
            if detect(data["description"][i]) == "en":
                data["description"][i] = await translator(data["color"][i])
        except LangDetectException:
            pass
    return render_template("item_page.html", data=data, count_records=len(data['id']))
