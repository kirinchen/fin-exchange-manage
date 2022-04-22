from model import Product
from service.order_dao import OrderDao
from service.product_dao import ProductDao


class FTXOrderDao(OrderDao):
    pass


def get_impl_clazz() -> FTXOrderDao:
    return FTXOrderDao
