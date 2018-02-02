from sqlalchemy import Column, Integer, String, Time, Boolean
from .db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    location = Column(String)
    notification_time = Column(Time)
    active = Column(Boolean, default=False)

    def __str__(self):
        return "User {0}".format(self.id)
