from model import Product
from service.product_dao import ProductDao


class BinanceProductDao(ProductDao):

    def refresh_product(self, p: Product):
        p.min_item = 1 / pow(10, p.precision_amount)
        self.update(p)


def get_impl_clazz() -> BinanceProductDao:
    return BinanceProductDao
