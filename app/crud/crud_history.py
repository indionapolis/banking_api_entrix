from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy.orm import aliased

from app.crud.base import CRUDBase

from ..models import Account
from ..models import History


class CRUDHistory(CRUDBase[History, History, History]):
    def filter_customer(self, db, customer_id) -> AbstractPage[History]:
        return paginate(
            db.query(self.model)
            .outerjoin(
                Account,
                and_(
                    History.from_account_id == Account.id,
                    Account.customer_id == customer_id,
                ),
            )
            .outerjoin(
                aliased(Account, name="to_account"),
                and_(
                    History.to_account_id == aliased(Account, name="to_account").id,
                    aliased(Account, name="to_account").customer_id == customer_id
                ),
            )
        )

    def filter_account(self, db, account_id) -> AbstractPage[History]:
        return paginate(
            db.query(self.model).filter(or_(History.from_account_id == account_id, History.to_account_id == account_id))
        )


history = CRUDHistory(History)
