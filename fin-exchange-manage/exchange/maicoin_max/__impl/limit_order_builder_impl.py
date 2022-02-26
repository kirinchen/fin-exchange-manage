from service.order_builder import LimitOrderBuilder


class MaxLimitOrderBuilder(LimitOrderBuilder):
    pass


def get_impl_clazz() -> MaxLimitOrderBuilder:
    return MaxLimitOrderBuilder
