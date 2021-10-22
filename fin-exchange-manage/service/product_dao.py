import abc
from typing import List

from sqlalchemy.orm import aliased

from model import Product, Item
from service.base_exchange_abc import BaseDao


class ProductDao(BaseDao):

    def refresh_all(self):
        ps: List[Product] = self.list_by_this_exchange()
        for p in ps:
            self.refresh_product(p)

    def list_by_this_exchange(self) -> List[Product]:
        return self.session.query(Product).filter(Product.exchange == self.exchange).all()

    def get_entity_clazz(self) -> Product:
        return Product

    def get_abc_clazz(self) -> object:
        return ProductDao

    def get_by_item_symbol(self, item_symbol: str, valuation_item_symbol: str) -> Product:
        item_table = aliased(Item)
        valuation_item_table = aliased(Item)

        return self.session.query(Product) \
            .join(item_table, Product.item == item_table.name) \
            .join(valuation_item_table, Product.valuation_item == valuation_item_table.name) \
            .filter(item_table.symbol == item_symbol) \
            .filter(valuation_item_table.symbol == valuation_item_symbol) \
            .filter(Product.exchange == self.exchange) \
            .one()

    def fix_precision_price(self, product: Product, price: float) -> float:
        fstr = str(product.precision_price) + 'f'
        return float(('{:.' + fstr + '}').format(price))

    def fix_precision_amt(self, product: Product, amt: float) -> float:
        fstr = str(product.precision_amount) + 'f'
        return float(('{:.' + fstr + '}').format(amt))

    @abc.abstractmethod
    def refresh_product(self, p: Product):
        raise NotImplementedError('refresh_product')
