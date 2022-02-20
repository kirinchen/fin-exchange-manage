from exchange.binance import binance_utils
from model import Product
from service.product_dao import ProductDao


class BinanceProductDao(ProductDao):

    def get_min_valuation_item_amount(self, product: Product, price: float) -> float:
        binance_symbol = binance_utils.convert_symbol_helper(product)
        return max(price * binance_symbol.get_amt_info().minQty, binance_symbol.get_price_info().minPrice)


def get_impl_clazz() -> BinanceProductDao:
    return BinanceProductDao
