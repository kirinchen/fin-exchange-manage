import abc
from typing import List

from sqlalchemy.orm import aliased

from model import Product, Item
from service.base_exchange_abc import BaseDao


class ProductDao(BaseDao):

    def list_by_this_exchange(self) -> List[Product]:
        return self.session.query(Product).filter(Product.exchange == self.exchange_name).all()

    def get_entity_clazz(self) -> Product:
        return Product

    def get_abc_clazz(self) -> object:
        return ProductDao

    def get_by_prd_name(self, prd_name: str) -> Product:
        return self.session.query(Product) \
            .filter(Product.exchange == self.exchange_name) \
            .filter(Product.prd_name == prd_name) \
            .one()

    def get_by_item_symbol(self, item_symbol: str, valuation_item_symbol: str) -> Product:
        item_table = aliased(Item)
        valuation_item_table = aliased(Item)

        return self.session.query(Product) \
            .join(item_table, Product.item == item_table.name) \
            .join(valuation_item_table, Product.valuation_item == valuation_item_table.name) \
            .filter(item_table.symbol == item_symbol) \
            .filter(valuation_item_table.symbol == valuation_item_symbol) \
            .filter(Product.exchange == self.exchange_name) \
            .one()

    @classmethod
    def fix_precision_price(cls, product: Product, price: float) -> float:
        fstr = str(product.precision_price) + 'f'
        return float(('{:.' + fstr + '}').format(price))

    @classmethod
    def fix_precision_amt(cls, product: Product, amt: float) -> float:
        fstr = str(product.precision_amount) + 'f'
        return float(('{:.' + fstr + '}').format(amt))

    def get_min_valuation_item_amount(self, product: Product, price: float) -> float:
        if product.min_item and product.min_valuation_item:
            return max(price * product.min_item, product.min_valuation_item)
        if product.min_item:
            return price * product.min_item
        if product.min_valuation_item:
            return product.min_valuation_item
        return 0
