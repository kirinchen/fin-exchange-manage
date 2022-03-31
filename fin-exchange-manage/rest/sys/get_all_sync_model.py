from typing import List

from sqlalchemy.orm import scoped_session

from infra import database
from model import Item, Product, product, Exchange
from utils import comm_utils


class Result:

    def __init__(self, items: List[Item], products: List[Product], exchanges: List[Exchange]):
        self.items: List[Item] = items
        self.products: List[Product] = products
        self.exchanges: List[Exchange] = exchanges


def run(payload: dict) -> dict:
    with database.session_scope() as session:
        session: scoped_session = session
        ans = Result(
            items=session.query(Item).all(),
            products=session.query(Product).all(),
            exchanges=session.query(Exchange).all(),
        )
        return comm_utils.to_dict(ans)
