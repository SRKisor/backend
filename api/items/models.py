from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime

from api import Base


class Items(Base):
    __tablename__ = 'items'

    id_ = Column(Integer, primary_key=True)
    item_code = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    qty = Column(Integer, nullable=False)
    retail_price = Column(Float(precision=2), nullable=False)
    wholesale_price = Column(Float(precision=2), nullable=False)
    discount = Column(Float(precision=2))
    mfd_date = Column(DateTime, nullable=False)
    exp_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
