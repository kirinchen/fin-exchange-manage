from infra.enums import OrderStatus
from service.position_fuse.fuse_builder import FixedStepFuseBuilder


class BinanceFixedStepFuseBuilder(FixedStepFuseBuilder):

    def is_manual_adjust_orders(self):
        for od in self.prepareData.orders:
            if od.status == OrderStatus.CANCELED:
                return True
            if od.status == OrderStatus.EXPIRED:
                return True
        return False


def get_impl_clazz() -> BinanceFixedStepFuseBuilder:
    return BinanceFixedStepFuseBuilder
