from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import func
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.account import Account


class History(Base):
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(precision=10, scale=2))

    timestamp = Column(DateTime(timezone=True), default=func.now())

    from_account_id = Column(Integer, ForeignKey(Account.id), nullable=False)
    from_account = relationship(
        "Account", backref="outcome_history", foreign_keys=[from_account_id]
    )

    to_account_id = Column(Integer, ForeignKey(Account.id), nullable=False)
    to_account = relationship(
        "Account", backref="income_history", foreign_keys=[to_account_id]
    )
