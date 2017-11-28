#!/usr/bin/env python3
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

self_path = os.path.dirname(os.path.realpath(__file__))
full_db_path = os.path.join(self_path, "tg.db")

engine = create_engine("sqlite:///" + full_db_path)

Session = sessionmaker(bind=engine)
Base = declarative_base(engine)

class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    city = Column(String, default="Kyiv")
    time = Column(String, default="07:00")
    active = Column(Boolean, default=True)

    def __str__(self):
        return "<User: id={}>".format(self.id)


if __name__ == "__main__" and not os.path.isfile(full_db_path):
    Base.metadata.create_all(engine)
    

