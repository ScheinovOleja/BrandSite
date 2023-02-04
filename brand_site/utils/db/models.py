from brand_site import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    article = db.Column(db.String(64))
    title = db.Column(db.String(256))
    subtitle = db.Column(db.String(256))
    color = db.Column(db.String(64), nullable=True, default='-')
    category = db.Column(db.String(128))
    images = db.Column(db.JSON)


class ZilliData(BaseModel):
    __tablename__ = 'zilli_data'

    more_details = db.Column(db.String(1024))
    materials = db.Column(db.String(1024))


class DiorData(BaseModel):
    __tablename__ = 'dior_data'

    size_and_fit = db.Column(db.String(512))


class LoropianaData(BaseModel):
    __tablename__ = 'loropiana_data'

    details = db.Column(db.String(1024))


class LouisData(BaseModel):
    __tablename__ = 'louisvuitton_data'

    description = db.Column(db.String(1024))


class ChanelData(BaseModel):
    __tablename__ = 'chanel_data'

    size = db.Column(db.String(64))


class BrunelloData(BaseModel):
    __tablename__ = 'brunello_data'

    details = db.Column(db.String(1024))


class BrioniData(BaseModel):
    __tablename__ = 'brioni_data'

    details = db.Column(db.String(1024))
    materials = db.Column(db.String(128))


class StefanoData(BaseModel):
    __tablename__ = 'stefano_data'

    details = db.Column(db.String(2048))


class BottegaData(BaseModel):
    __tablename__ = 'bottega_data'

    details = db.Column(db.String(1024))


class CelineData(BaseModel):
    __tablename__ = 'celine_data'

    details = db.Column(db.String(1024))


class LaurentData(BaseModel):
    __tablename__ = 'laurent_data'

    details = db.Column(db.String(1024))


class FordData(BaseModel):
    __tablename__ = 'ford_data'

    details = db.Column(db.String(1024))
