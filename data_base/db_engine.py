from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.basic_config import settings


SQLALCHEMY_DATABASE_URL = settings.db_settings.url

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autoflush=False, bind=engine)
