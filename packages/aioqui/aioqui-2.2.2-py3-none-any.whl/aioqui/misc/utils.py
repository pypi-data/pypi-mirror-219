from functools import cache, wraps
from typing import Awaitable, Any, Callable


class _CachedAwaitable:
    _ResultUnset: str = 'CachedAwaitableResultUnset'

    def __init__(self, awaitable: Awaitable):
        self.awaitable: Awaitable = awaitable
        self.result: Any = _CachedAwaitable._ResultUnset

    def __await__(self) -> Any:
        if self.result == _CachedAwaitable._ResultUnset:
            self.result = yield from self.awaitable.__await__()
        return self.result


def _reawaitable(func: Callable, /):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return _CachedAwaitable(func(*args, **kwargs))
    return wrapper


def aiocache(func: Callable, /):
    return cache(_reawaitable(func))
