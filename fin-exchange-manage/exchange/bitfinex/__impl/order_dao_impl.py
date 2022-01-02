from model import Product
from service.order_dao import OrderDao
from service.product_dao import ProductDao


class BinanceOrderDao(OrderDao):
    pass


def get_impl_clazz() -> BinanceOrderDao:
    return BinanceOrderDao
