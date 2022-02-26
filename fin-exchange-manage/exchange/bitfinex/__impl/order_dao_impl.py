from model import Product
from service.order_dao import OrderDao
from service.product_dao import ProductDao


class BitfinexOrderDao(OrderDao):
    pass


def get_impl_clazz() -> BitfinexOrderDao:
    return BitfinexOrderDao
