from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import datetime

from api import Base


class Bills(Base):
    """
        Table structure for "bills" Table
    """

    __tablename__ = 'bills'

    id_ = Column(Integer, primary_key=True)
    bill_number = Column(String, nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id_"), nullable=False)
    cashier = Column(String, nullable=False)
    paid = Column(Boolean, nullable=False)
    date = Column(DateTime, nullable=False)
    amount = Column(Float(precision=2), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    client = relationship("Clients", backref="bills", uselist=False)
