from typing import List

from maicoin_max.client import Client
from maicoin_max.dto.market import MarketInfo

from exchange.maicoin_max import gen_request_client, max_utils
from model import Product
from service.product_dao import ProductDao
from service.sync_cron import SyncCron
from utils import comm_utils


def _get_symbol_info(prd_name: str, ms: List[MarketInfo]) -> MarketInfo:
    prd_name = max_utils.unfix_symbol(prd_name)
    return [m for m in ms if m.id == prd_name][0]


def sync_product(p: Product, product_dao: ProductDao, ms: List[MarketInfo]):
    m_info = _get_symbol_info(p.prd_name, ms)
    p.set_config(comm_utils.to_dict(m_info))
    product_dao.update(p)


class MaxSyncCron(SyncCron):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client: Client = gen_request_client()

    def init_bind_load(self):
        result: List[MarketInfo] = self.client.get_public_all_markets()
        self.sync_all_product(result)

    def sync_all_product(self, symbols: List[MarketInfo]):
        p_dao: ProductDao = self.get_ex_obj(ProductDao)
        ps: List[Product] = p_dao.list_by_this_exchange()
        for p in ps:
            sync_product(p, p_dao, symbols)


def get_impl_clazz() -> MaxSyncCron:
    return MaxSyncCron
