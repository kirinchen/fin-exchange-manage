from service.position_fuse.stop_loss import StopLoss


class BinanceStopLoss(StopLoss):
    pass


def get_impl_clazz() -> StopLoss:
    return StopLoss
