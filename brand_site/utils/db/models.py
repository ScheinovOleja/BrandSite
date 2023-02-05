from server import db


class BrandsData(db.Model):
    __tablename__ = "brands_data"
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    article = db.Column(db.String(64))
    title = db.Column(db.String(256))
    subtitle = db.Column(db.String(256))
    color = db.Column(db.String(64), nullable=True, default='')
    category = db.Column(db.String(128))
    materials = db.Column(db.String(1024), nullable=True, default='')
    details = db.Column(db.String(2048), nullable=True, default='')
    size_and_fit = db.Column(db.String(512), nullable=True, default='')
    description = db.Column(db.String(1024), nullable=True, default='')
    brand = db.Column(db.String(32))
    images = db.Column(db.JSON)


class AllBrands(db.Model):
    __tablename__ = "all_brands"
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))
    short_name = db.Column(db.String(32))
