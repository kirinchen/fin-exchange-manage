from model import Product
from service.product_dao import ProductDao
from service.sync_cron import SyncCron


class BitfinexSyncCron(SyncCron):
    pass


def get_impl_clazz() -> BitfinexSyncCron:
    return BitfinexSyncCron
