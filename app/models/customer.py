from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .account import Account  # noqa: F401


class Customer(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)

    accounts = relationship("Account", backref="customer")
