from abc import ABC
from typing import List

from utils.order_utils import OrderFilter, OrdersInfo


class OrderClientService(ABC):

    def query_order(self,exchange:str,filter:OrderFilter) -> OrdersInfo:
        pass