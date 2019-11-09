from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime

from api import Base


class Clients(Base):
    """
        Table structure for "clients" Table
    """

    __tablename__ = 'clients'

    id_ = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
