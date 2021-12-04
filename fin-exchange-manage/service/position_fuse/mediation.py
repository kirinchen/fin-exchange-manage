from typing import List

from sqlalchemy.orm import Session

from service.base_exchange_abc import BaseExchangeAbc
from service.order_client_service import OrderClientService
from service.position_fuse import stoper, dtos
from service.position_fuse.stop_loss import StopLossDto, StopLoss
from service.position_fuse.stop_trailing import StopTrailingDto, StopTrailing
from utils import order_utils


class StopMediationDto:

    def __init__(self, symbol: str, positionSide: str, tags: List[str], stopLoss: dict, stopTrailing: dict, **kwargs):
        self.symbol: str = symbol
        self.positionSide: str = positionSide
        self.tags: List[str] = tags
        self._apply_default_fields(stopLoss)
        self.stopLoss = StopLossDto(**stopLoss)
        self._apply_default_fields(stopTrailing)
        self.stopTrailing = StopTrailingDto(**stopTrailing)

    def _apply_default_fields(self, dto: dict):
        dto.update({
            'symbol': self.symbol,
            'positionSide': self.positionSide,
            'tags': self.tags
        })


class StopMediation(BaseExchangeAbc):

    def __init__(self, exchange_name: str, session: Session = None):
        super(StopMediation, self).__init__(exchange_name, session)
        self.dto: StopMediationDto = None
        self.stopLoss: StopLoss = None
        self.stopTrailing: StopTrailing = None
        self.orderClientService: OrderClientService = None

    def get_abc_clazz(self) -> object:
        return StopMediation

    def init(self, dto: StopMediationDto):
        self.dto: StopMediationDto = dto
        self.orderClientService: OrderClientService = self.get_ex_obj(OrderClientService)
        self.stopLoss: StopLoss = self.get_ex_obj(StopLoss).init(dto=self.dto.stopLoss)
        self.stopTrailing: StopTrailing = self.get_ex_obj(StopTrailing).init(dto=self.dto.stopTrailing)

    def stop(self) -> List[dtos.StopResult]:
        if self.stopLoss.no_position:
            return [dtos.StopResult(stopState=dtos.StopState.NO_POS, noActiveMsg='no_position')]
        return self._stop_each([self.stopTrailing, self.stopLoss])

    def _stop_each(self, stops: List[stoper.Stoper]) -> List[dtos.StopResult]:
        no_stop_results: List[dtos.StopResult] = list()
        all_orders = self.orderClientService.list_all_order(symbol=self.dto.symbol)
        for stop in stops:
            stop.load_vars(all_orders)
            stop_result: dtos.StopResult = stop.run()
            no_stop_results.append(stop_result)

        return no_stop_results
