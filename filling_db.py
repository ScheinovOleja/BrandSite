import json

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from parser.models import BrandsData, AllBrands

if __name__ == '__main__':
    with open('test.json', 'r') as file:
        data = json.load(file)
    engine = create_engine('postgresql+psycopg2://oleg:oleg2000@localhost/parser_brands')
    with Session(engine) as session:
        for item in data['values']:
            session.add(AllBrands(**item))
        session.commit()
    print('yeryer')

