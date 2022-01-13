from typing import List

from sqlalchemy.orm import Session

from binance_f import RequestClient
from binance_f.model import Order, TimeInForce, OrderType, WorkingType
from dto.order_dto import OrderDto
from exchange.binance import gen_request_client, binance_utils
from model.init_data import init_item
from service.order_client_service import OrderClientService
from service.product_dao import ProductDao
from utils import comm_utils, direction_utils

MAX_BATCH_COUNT = 7


class BinanceOrderClientService(OrderClientService):

    def __init__(self, exchange_name: str, session: Session = None):
        super(BinanceOrderClientService, self).__init__(exchange_name, session)
        self.client: RequestClient = gen_request_client()

    def list_all_order(self, prd_name: str, orderId: int = None, startTime: int = None, endTime: int = None,
                       limit: int = None) -> List[OrderDto]:
        oods: List[Order] = self.client.get_all_orders(symbol=binance_utils.fix_usdt_symbol(prd_name), limit=limit,
                                                       startTime=startTime, endTime=endTime, orderId=orderId)
        return [binance_utils.convert_order_dto(o) for o in oods]

    def cancel_list_orders(self, symbol: str, currentOds: List[OrderDto]) -> List[OrderDto]:
        ids: List[str] = [od.orderId for od in currentOds]
        batch_ids: List[str] = list()
        results: List[OrderDto] = list()
        count = 0
        for oid in ids:
            count = count + 1
            batch_ids.append(oid)
            if count == MAX_BATCH_COUNT:
                results.extend(self.client.cancel_list_orders(symbol=binance_utils.fix_usdt_symbol(symbol),
                                                              orderIdList=batch_ids))

                count = 0
                batch_ids.clear()

        if len(batch_ids) > 0:
            results.extend(self.client.cancel_list_orders(symbol=binance_utils.fix_usdt_symbol(symbol),
                                                          orderIdList=batch_ids))
        return results

    def post_limit(self, prd_name: str, price: float, quantity: float, positionSide: str, tags: List[str]) -> OrderDto:
        product = self.productDao.get_by_prd_name(prd_name)
        amt = self.positionClient.get_max_order_amt(symbol=prd_name, positionSide=positionSide, price=price)
        quantity = min(amt, quantity)
        price = ProductDao.fix_precision_price(product, price)
        if price <= 0:
            return None
        price_str = str(price)
        p_amt: float = ProductDao.fix_precision_amt(product, quantity)
        if p_amt == 0:
            return None
        quantity_str = str(p_amt)
        side = direction_utils.get_limit_order_side(positionSide)
        ans = self.client.post_order(price=price_str,
                                     side=side,
                                     symbol=binance_utils.fix_usdt_symbol(prd_name),
                                     timeInForce=TimeInForce.GTC,
                                     ordertype=OrderType.LIMIT,
                                     workingType=WorkingType.CONTRACT_PRICE,
                                     positionSide=positionSide,
                                     # activationPrice=None,
                                     # closePosition=False,
                                     quantity=quantity_str,
                                     newClientOrderId=comm_utils.get_order_cid(tags=tags)
                                     )
        return binance_utils.convert_order_dto(ans)

    def post_stop_market(self, prd_name: str, price: float, quantity: float, positionSide: str,
                         tags: List[str]) -> OrderDto:

        if quantity == 0:
            return None
        product = self.productDao.get_by_prd_name(prd_name)
        price = ProductDao.fix_precision_price(product, price)
        if price <= 0:
            return None
        price_str = str(price)
        p_amt: float = ProductDao.fix_precision_amt(product, quantity)
        p_amt = p_amt if p_amt > 0 else product.min_item
        quantity_str = str(p_amt)
        side = direction_utils.get_stop_order_side(positionSide)
        result = self.client.post_order(
            side=side,
            symbol=binance_utils.fix_usdt_symbol(prd_name),
            timeInForce=TimeInForce.GTC,
            ordertype=OrderType.STOP_MARKET,
            workingType=WorkingType.CONTRACT_PRICE,
            positionSide=positionSide,
            stopPrice=price_str,
            quantity=quantity_str,
            # closePosition=True,
            newClientOrderId=comm_utils.get_order_cid(tags)
        )
        return binance_utils.convert_order_dto(result)

    def post_take_profit(self, prd_name: str, price: float, quantity: float, positionSide: str,
                         tags: List[str]) -> OrderDto:
        if quantity == 0:
            return None
        product = self.productDao.get_by_prd_name(prd_name)
        price = ProductDao.fix_precision_price(product, price)
        if price <= 0:
            return None
        price_str = str(price)
        p_amt: float = ProductDao.fix_precision_amt(product, quantity)
        p_amt = p_amt if p_amt > 0 else product.min_item
        quantity_str = str(p_amt)
        side = direction_utils.get_stop_order_side(positionSide)
        result = self.client.post_order(
            side=side,
            symbol=binance_utils.fix_usdt_symbol(prd_name),
            timeInForce=TimeInForce.GTC,
            ordertype=OrderType.TAKE_PROFIT_MARKET,
            workingType=WorkingType.CONTRACT_PRICE,
            positionSide=positionSide,
            stopPrice=price_str,
            quantity=quantity_str,
            newClientOrderId=comm_utils.get_order_cid(tags)
        )
        return binance_utils.convert_order_dto(result)


def get_impl_clazz() -> BinanceOrderClientService:
    return BinanceOrderClientService
