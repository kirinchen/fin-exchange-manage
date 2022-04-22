from service.order_pack_dao import OrderPackDao


class FTXOrderPackDao(OrderPackDao):
    pass


def get_impl_clazz() -> FTXOrderPackDao:
    return FTXOrderPackDao
