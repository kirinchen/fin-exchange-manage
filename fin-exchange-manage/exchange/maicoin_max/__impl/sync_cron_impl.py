from model import Product
from service.product_dao import ProductDao
from service.sync_cron import SyncCron


class BinanceSyncCron(SyncCron):

    def sync_product(self, p: Product, product_dao: ProductDao):
        p.min_item = 1 / pow(10, p.precision_amount)
        product_dao.update(p)


def get_impl_clazz() -> BinanceSyncCron:
    return BinanceSyncCron
