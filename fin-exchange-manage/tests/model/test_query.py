from sqlalchemy.orm import Session

from infra import database
from model import Product


def test_query():
    with database.session_scope() as session:
        session: Session = session
        result = session.query(Product).filter(_gen_prd_condition()).all()
        print(result)


def _gen_prd_condition():
    return Product.prd_name == 'BTC'
