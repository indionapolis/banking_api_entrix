from ..models import Account
from ..models import Customer
from .base import CRUDBase
from .crud_employee import employee
from .crud_history import history

account = CRUDBase[Account, Account, Account](Account)
customer = CRUDBase[Customer, Customer, Customer](Customer)
