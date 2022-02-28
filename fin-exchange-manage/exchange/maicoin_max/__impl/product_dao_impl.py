from maicoin_max.dto.market import MarketInfo

from model import Product
from service.product_dao import ProductDao


class MaxProductDao(ProductDao):

    def get_min_valuation_item_amount(self, product: Product, price: float) -> float:
        m_info = MarketInfo(**product.get_config())
        return m_info.min_quote_amount


def get_impl_clazz() -> MaxProductDao:
    return MaxProductDao
