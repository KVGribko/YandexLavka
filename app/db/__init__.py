from sqlalchemy_utils import create_database, database_exists

from app.models import courier, order, region  # noqa: F401

from .base import Base, engine

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)
