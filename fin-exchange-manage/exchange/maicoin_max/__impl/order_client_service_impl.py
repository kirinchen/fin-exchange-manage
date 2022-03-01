from typing import List, Any

from maicoin_max.client import Client
from maicoin_max.dto.market import MarketInfo

from dto.order_dto import OrderDto
from exchange.maicoin_max import gen_request_client, max_utils
from infra.enums import PositionSide
from service.order_client_service import OrderClientService
from utils import comm_utils


class MaxOrderClientService(OrderClientService):

    def __init__(self, **kwargs):
        super(MaxOrderClientService, self).__init__(**kwargs)
        self.client: Client = gen_request_client()

    def list_all_order(self, prd_name: str, orderId: int = None, startTime: int = None, endTime: int = None,
                       limit: int = None) -> List[OrderDto]:
        oods: List[Any] = self.client.get_private_order_history(pair=max_utils.unfix_symbol(prd_name), state=["done"])
        return [max_utils.convert_order_dto(od) for od in oods]

    def cancel_list_orders(self, symbol: str, currentOds: List[OrderDto]) -> List[OrderDto]:
        pass  # TODO

    def post_limit(self, prd_name: str, onMarketPrice: bool, price: float, quantity: float, positionSide: str,
                   tags: List[str]) -> OrderDto:
        product = self.productDao.get_by_prd_name(prd_name)
        pair = max_utils.unfix_symbol(prd_name)
        m_info = MarketInfo(**product.get_config())
        amt = max_utils.fix_amount(m_info=m_info, amt=quantity, curPrice=price)
        if amt <= 0:
            return None
        side = 'buy' if positionSide == PositionSide.LONG else 'sell'
        fixed_price = '' if onMarketPrice else comm_utils.fix_precision(m_info.quote_unit_precision, price)
        order_type: str = 'market' if onMarketPrice else 'limit'
        client_uid = comm_utils.get_order_cid(tags=tags)

        o = self.client.set_private_create_order(pair=pair, side=side, amount=amt,
                                                 price=fixed_price,
                                                 _type=order_type, client_id=client_uid)
        return max_utils.convert_order_dto(o)

    def post_stop_market(self, prd_name: str, price: float, quantity: float, positionSide: str,
                         tags: List[str]) -> OrderDto:
        product = self.productDao.get_by_prd_name(prd_name)
        pair = max_utils.unfix_symbol(prd_name)
        m_info = MarketInfo(**product.get_config())
        amt = max_utils.fix_amount(m_info=m_info, amt=quantity, curPrice=price)
        if amt <= 0:
            return None
        side = 'buy' if positionSide == PositionSide.LONG else 'sell'
        fixed_price = comm_utils.fix_precision(m_info.quote_unit_precision, price)
        order_type: str =  'limit'
        client_uid = comm_utils.get_order_cid(tags=tags)

        o = self.client.set_private_create_order(pair=pair, side=side, amount=amt,
                                                 price=fixed_price,
                                                 _type=order_type, client_id=client_uid)
        return max_utils.convert_order_dto(o)

    def post_take_profit(self, prd_name: str, price: float, quantity: float, positionSide: str,
                         tags: List[str]) -> OrderDto:
        pass  # TODO


def get_impl_clazz() -> MaxOrderClientService:
    return MaxOrderClientService
