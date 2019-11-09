from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import datetime

from api import Base


class Payment_Types(Base):
    __tablename__ = 'payment_types'

    id_ = Column(Integer, primary_key=True)
    type_name = Column(String, nullable=False)


class Payment_Methods(Base):
    __tablename__ = 'payment_methods'

    id_ = Column(Integer, primary_key=True)
    method_name = Column(String, nullable=False)


class Payments(Base):
    __tablename__ = 'payments'

    id_ = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    amount = Column(Float(precision=2), nullable=False)
    paid = Column(Boolean, nullable=False)
    id_payment_type = Column(Integer, ForeignKey(
        "payment_types.id_"), nullable=False)
    id_payment_method = Column(Integer, ForeignKey(
        "payment_methods.id_"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    payment_types = relationship(
        "Payment_Types", backref="payments", uselist=False)
    payment_methods = relationship(
        "Payment_Methods", backref="payments", uselist=False)
