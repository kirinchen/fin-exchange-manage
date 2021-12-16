from typing import Any


def merge(src: dict, tar: object) -> object:
    for k, v in tar.__dict__.items():
        k: str = k
        if k.startswith('_'):
            continue
        setattr(tar, k, src.get(k, v))

    return tar


def getval(src: object, key: str, default: Any = None) -> Any:
    if type(src) == dict:
        src: dict = src
        return src.get(key, default)
    else:
        return getattr(src, key, default)


def setval(src: object, key: str, val: Any):
    if type(src) == dict:
        src: dict = src
        src[key] = val
    else:
        setattr(src, key, val)
