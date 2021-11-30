from service.position_fuse.stop_trailing import StopTrailing


class BinanceStopTrailing(StopTrailing):
    pass


def get_impl_clazz() -> BinanceStopTrailing:
    return BinanceStopTrailing
