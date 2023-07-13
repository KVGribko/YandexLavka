import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.api.depends import get_db
from app.db import Base
from app.main import app

load_dotenv()

TEST_DATA_BASE_URL = os.getenv(
    "POSTGRES_DSN" + "_test",
    default="postgresql://postgres:password@localhost:5432/postgres_test",
)

# TEST_DATA_BASE_URL = "postgresql://postgres:password@localhost:32700/postgres_test"


@pytest.fixture(scope="session")
def db_engine():
    try:
        engine = create_engine(TEST_DATA_BASE_URL, pool_pre_ping=True)
        if database_exists(engine.url):
            drop_database(engine.url)
        create_database(engine.url)
        Base.metadata.create_all(engine)
        yield engine
    finally:
        drop_database(TEST_DATA_BASE_URL)
        # pass


@pytest.fixture(scope="function")
def db(db_engine):
    try:
        TestingSessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=db_engine
        )
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as test_client:
        yield test_client


pytest_plugins = ["tests.fixtures.fixture_courier", "tests.fixtures.fixture_order"]
