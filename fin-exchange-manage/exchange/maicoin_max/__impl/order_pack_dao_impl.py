from service.order_pack_dao import OrderPackDao


class BinanceOrderPackDao(OrderPackDao):
    pass


def get_impl_clazz() -> BinanceOrderPackDao:
    return BinanceOrderPackDao
