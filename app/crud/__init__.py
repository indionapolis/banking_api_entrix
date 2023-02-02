from ..models import Account
from ..models import Customer
from ..schemas import InAccount
from ..schemas import InCustomer
from .base import CRUDBase
from .crud_employee import employee
from .crud_history import history

account = CRUDBase[Account, InAccount, InAccount](Account)
customer = CRUDBase[Customer, InCustomer, InCustomer](Customer)
