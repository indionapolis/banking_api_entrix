from typing import Any

from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase

from ..models import Account
from ..models import History
from ..schemas import HistoryOut


class CRUDHistory(CRUDBase[History, HistoryOut, HistoryOut]):
    def filter_customer(self, db: Session, customer_id: Any) -> AbstractPage[History]:
        q1 = db.query(self.model).join(
            Account,
            and_(
                History.from_account_id == Account.id,
                Account.customer_id == customer_id,
            ),
        )
        q2 = db.query(self.model).join(
            Account,
            and_(
                History.to_account_id == Account.id,
                Account.customer_id == customer_id,
            ),
        )

        return paginate(q1.union(q2))

    def filter_account(self, db: Session, account_id: Any) -> AbstractPage[History]:
        return paginate(
            db.query(self.model).filter(
                or_(
                    History.from_account_id == account_id,
                    History.to_account_id == account_id,
                )
            )
        )


history = CRUDHistory(History)
