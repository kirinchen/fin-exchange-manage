from maicoin_max.client import Client

from exchange.maicoin_max import gen_request_client
from model import Product
from service.product_dao import ProductDao
from service.sync_cron import SyncCron


class MaxSyncCron(SyncCron):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client: Client = gen_request_client()

    def init_bind_load(self):
        result = self.client.get_public_all_markets()
        print(result)
        # self.sync_all_product(symbols)

    # def sync_all_product(self, symbols: List[Symbol]):
    #     p_dao: ProductDao = self.get_ex_obj(ProductDao)
    #     ps: List[Product] = p_dao.list_by_this_exchange()
    #     for p in ps:
    #         sync_product(p, p_dao, symbols)


def get_impl_clazz() -> MaxSyncCron:
    return MaxSyncCron
