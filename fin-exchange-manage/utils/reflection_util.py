from typing import Any


def merge(src: object, tar: object) -> object:
    for k, v in tar.__dict__.items():
        k: str = k
        if k.startswith('_'):
            continue
        if not has_key(src, k):
            continue
        setattr(tar, k, getval(src, k, v))

    return tar


def has_key(src: object, key: str) -> bool:
    if type(src) == dict:
        src: dict = src
        return key in src
    else:
        return hasattr(src, key)


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
