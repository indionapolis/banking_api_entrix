from ..models import Account
from ..models import Customer
from ..models import History
from .base import CRUDBase
from .crud_employee import employee

account = CRUDBase[Account, Account, Account](Account)
customer = CRUDBase[Customer, Customer, Customer](Customer)
history = CRUDBase[History, History, History](History)
