from model import Product
from service.product_dao import ProductDao


class BitfinexProductDao(ProductDao):
    pass


def get_impl_clazz() -> BitfinexProductDao:
    return BitfinexProductDao
