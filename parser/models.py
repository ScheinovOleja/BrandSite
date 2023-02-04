from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BrandsData(Base):
    __tablename__ = "brands_data"
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    article = Column(String(64))
    title = Column(String(256))
    subtitle = Column(String(256))
    color = Column(String(64), nullable=True, default='-')
    category = Column(String(128))
    materials = Column(String(1024), nullable=True, default='')
    details = Column(String(2048), nullable=True, default='')
    size_and_fit = Column(String(512), nullable=True, default='')
    description = Column(String(1024), nullable=True, default='')
    brand = Column(String(32))
    images = Column(JSON())


class AllBrands(Base):
    __tablename__ = "all_brands"
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(32))
    short_name = Column(String(32))


def get_or_create(session, model, defaults=None, **kwargs):
    """
    Get or create a model instance while preserving integrity.
    """
    try:
        return session.query(model).filter_by(**kwargs).one(), False
    except NoResultFound:
        if defaults is not None:
            kwargs.update(defaults)
        try:
            with session.begin_nested():
                instance = model(**kwargs)
                session.add(instance)
                return instance, True
        except IntegrityError:
            return session.query(model).filter_by(**kwargs).one(), False


# class ZilliData(BaseModel):
#     __tablename__ = 'zilli_data'
#
#     more_details = Column(String(1024))
#     materials = Column(String(1024))
#
#
# class DiorData(BaseModel):
#     __tablename__ = 'dior_data'
#
#     size_and_fit = Column(String(512))
#
#
# class LoropianaData(BaseModel):
#     __tablename__ = 'loropiana_data'
#
#     details = Column(String(1024))
#
#
# class LouisData(BaseModel):
#     __tablename__ = 'louisvuitton_data'
#
#     description = Column(String(1024))
#
#
# class ChanelData(BaseModel):
#     __tablename__ = 'chanel_data'
#
#     size = Column(String(64))
#
#
# class BrunelloData(BaseModel):
#     __tablename__ = 'brunello_data'
#
#     details = Column(String(1024))
#
#
# class BrioniData(BaseModel):
#     __tablename__ = 'brioni_data'
#
#     details = Column(String(1024))
#     materials = Column(String(128))
#
#
# class StefanoData(BaseModel):
#     __tablename__ = 'stefano_data'
#
#     details = Column(String(2048))
#
#
# class BottegaData(BaseModel):
#     __tablename__ = 'bottega_data'
#
#     details = Column(String(1024))
#
#
# class CelineData(BaseModel):
#     __tablename__ = 'celine_data'
#
#     details = Column(String(1024))
#
#
# class LaurentData(BaseModel):
#     __tablename__ = 'laurent_data'
#
#     details = Column(String(1024))
#
#
# class FordData(BaseModel):
#     __tablename__ = 'ford_data'
#
#     details = Column(String(1024))
