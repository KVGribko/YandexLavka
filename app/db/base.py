import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv(
    "POSTGRES_DSN", default="postgresql://postgres:password@localhost:5432/postgres"
)

# DATABASE_URL = os.getenv(
#     "POSTGRES_DSN", default="postgresql://postgres:password@localhost:32700/postgres"
# )

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
