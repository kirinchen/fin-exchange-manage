from service.order_batch_dao import OrderBatchDao


class BinanceOrderBatchDao(OrderBatchDao):
    pass


def get_impl_clazz() -> BinanceOrderBatchDao:
    return BinanceOrderBatchDao
