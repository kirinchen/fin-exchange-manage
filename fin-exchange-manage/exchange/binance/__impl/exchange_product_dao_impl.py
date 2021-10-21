from service.exchange_product_dao import ExchangeProductDao


class BinanceExchangeProductDao(ExchangeProductDao):
    pass


def get_impl_clazz() -> BinanceExchangeProductDao:
    return BinanceExchangeProductDao
