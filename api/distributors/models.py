from sqlalchemy import Column, Integer, String, DateTime
import datetime

from api import Base


class Distributors(Base):
    __tablename__ = 'distributors'

    id_ = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
