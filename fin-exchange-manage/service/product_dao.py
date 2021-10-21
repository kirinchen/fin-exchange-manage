from model import Product, Item
from service.base_exchange_abc import BaseDao


class ProductDao(BaseDao):

    def get_entity_clazz(self) -> Product:
        return Product

    def get_abc_clazz(self) -> object:
        return ProductDao

    def get_by_item_symbol(self, item_symbol: str, valuation_item_symbol: str)->Product:
        self.session.query(Item).

    def fix_precision_price(self, product: Product, price: float) -> float:
        fstr = str(product.precision_price) + 'f'
        return float(('{:.' + fstr + '}').format(price))

    def fix_precision_amt(self, product: Product, amt: float) -> float:
        fstr = str(product.precision_amount) + 'f'
        return float(('{:.' + fstr + '}').format(amt))
