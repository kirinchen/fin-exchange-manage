from sqlalchemy.orm import scoped_session

from service.base_exchange_abc import BaseExchangeAbc


class ExchangeProductService(BaseExchangeAbc):

    def __init__(self, exchange_name: str):
        super(ExchangeProductService, self).__init__(exchange_name)
        self.session: scoped_session = None

    def get_abc_clazz(self) -> object:
        return ExchangeProductService

    def init(self, session: scoped_session):
        self.session = session


