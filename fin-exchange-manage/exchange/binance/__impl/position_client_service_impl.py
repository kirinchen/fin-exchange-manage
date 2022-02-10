from typing import List

from sqlalchemy.orm import Session

from binance_f import RequestClient
from binance_f.model import Position, TimeInForce, OrderType, WorkingType
from dto.position_dto import PositionDto
from exchange.binance import gen_request_client, binance_utils
from service.position_client_service import PositionClientService
from service.product_dao import ProductDao
from utils import direction_utils, comm_utils


class BinancePositionClientService(PositionClientService):

    def __init__(self, **kwargs):
        super(BinancePositionClientService, self).__init__(**kwargs)
        self.client: RequestClient = gen_request_client()

    def list_all(self) -> List[PositionDto]:
        result: List[Position] = self.client.get_position()
        return [binance_utils.convert_position_dto(op) for op in result]

    def close(self, prd_name: str, positionSide: str, amount: float) -> any:

        product = self.productDao.get_by_prd_name(prd_name)
        p_amt: float = ProductDao.fix_precision_amt(product, amount)
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
            stopPrice=40000,
            quantity=quantity_str,
            closePosition=True
        )
        return binance_utils.convert_order_dto(result)


def get_impl_clazz() -> BinancePositionClientService:
    return BinancePositionClientService
