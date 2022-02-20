from typing import List

from binance_f import RequestClient
from binance_f.model import ExchangeInformation
from binance_f.model.exchangeinformation import Symbol

from exchange.binance import gen_request_client, binance_utils
from model import Product
from service.product_dao import ProductDao
from service.sync_cron import SyncCron
from utils import comm_utils


def _get_symbol_info(prd_name: str, symbols: List[Symbol]) -> Symbol:
    symbol = binance_utils.fix_usdt_symbol(prd_name)
    return [sbl for sbl in symbols if sbl.symbol == symbol][0]


class BinanceSyncCron(SyncCron):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client: RequestClient = gen_request_client()

    def init_bind_load(self):
        result: ExchangeInformation = self.client.get_exchange_information()
        symbols: List[Symbol] = result.symbols
        self.sync_all_product(symbols)

    def sync_all_product(self, symbols: List[Symbol]):
        p_dao: ProductDao = self.get_ex_obj(ProductDao)
        ps: List[Product] = p_dao.list_by_this_exchange()
        for p in ps:
            self.sync_product(p, p_dao, symbols)

    def sync_product(self, p: Product, product_dao: ProductDao, symbols: List[Symbol]):
        sbl_info = _get_symbol_info(p.prd_name, symbols)
        p.set_config(comm_utils.to_dict(sbl_info))
        product_dao.update(p)


def get_impl_clazz() -> BinanceSyncCron:
    return BinanceSyncCron
