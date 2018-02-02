from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from .settings import DATABASE_URI

if not database_exists(DATABASE_URI):
    create_database(DATABASE_URI)

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base(engine)
