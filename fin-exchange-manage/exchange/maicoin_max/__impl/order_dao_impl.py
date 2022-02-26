from model import Product
from service.order_dao import OrderDao
from service.product_dao import ProductDao


class MaxOrderDao(OrderDao):
    pass


def get_impl_clazz() -> MaxOrderDao:
    return MaxOrderDao
