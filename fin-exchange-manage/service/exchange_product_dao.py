from model import ExchangeProduct
from service.base_exchange_abc import BaseDao


class ExchangeProductDao(BaseDao):

    def get_entity_clazz(self) -> ExchangeProduct:
        return ExchangeProduct

    def get_abc_clazz(self) -> object:
        return ExchangeProductDao

    def fix_precision_price(self, product: ExchangeProduct, price: float) -> float:
        fstr = str(product.precision_price) + 'f'
        return float(('{:.' + fstr + '}').format(price))

    def fix_precision_amt(self, product: ExchangeProduct,amt: float) -> float:
        fstr = str(product.precision_amount) + 'f'
        return float(('{:.' + fstr + '}').format(amt))
