from service.product_dao import ProductDao


class BinanceProductDao(ProductDao):
    pass


def get_impl_clazz() -> BinanceProductDao:
    return BinanceProductDao
