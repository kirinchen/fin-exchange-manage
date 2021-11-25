from service.position_fuse.mediation import StopMediation


class BinanceStopMediation(StopMediation):
    pass


def get_impl_clazz() -> BinanceStopMediation:
    return BinanceStopMediation
