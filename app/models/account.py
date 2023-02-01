from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric

from app.db.base_class import Base
from app.models.customer import Customer


class Account(Base):
    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Numeric(precision=10, scale=2), server_default="0.00")

    customer_id = Column(Integer, ForeignKey(Customer.id))
