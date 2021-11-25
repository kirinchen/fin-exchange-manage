from service.position_fuse.stop_guaranteed import StopGuaranteed


class BinanceStopGuaranteed(StopGuaranteed):
    pass


def get_impl_clazz() -> BinanceStopGuaranteed:
    return BinanceStopGuaranteed
