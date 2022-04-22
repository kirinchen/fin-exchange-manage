from model import Product
from service.product_dao import ProductDao
from service.sync_cron import SyncCron


class FTXSyncCron(SyncCron):
    pass


def get_impl_clazz() -> FTXSyncCron:
    return FTXSyncCron
