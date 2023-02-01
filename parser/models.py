from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    article = Column(String(64))
    title = Column(String(256))
    subtitle = Column(String(256))
    colors = Column(String(64), nullable=True, default='-')
    category = Column(String(128))
    images = Column(JSON())


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


class ZilliData(BaseModel):
    __tablename__ = 'zilli_data'

    more_details = Column(String(1024))
    materials = Column(String(1024))


class DiorData(BaseModel):
    __tablename__ = 'dior_data'

    size_and_fit = Column(String(512))


class LoropianaData(BaseModel):
    __tablename__ = 'loropiana_data'

    details = Column(String(512))
