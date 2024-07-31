"""
This module implements conditional versions of lru_cache and Django's cached_property
decorators. The conditional versions allow the cache to be disabled by setting a flag.
"""

from functools import lru_cache
from typing import Any, Callable
from django.utils.functional import cached_property

__all__ = (
    "set_functional_cache",
    "conditional_cached_property",
    "conditional_cache",
    "conditional_lru_cache",
)

cache_state = True


def set_functional_cache(state: bool = True):
    global cache_state
    cache_state = state


# noinspection PyPep8Naming
class conditional_cached_property(cached_property):
    """
    Decorator that conditionally converts a method with a single self argument into a
    property cached on the instance.

    A cached property can be made out of an existing method:
    (e.g. ``url = cached_property(get_absolute_url)``).
    """

    def __get__(self, instance, cls=None):
        """
        Call the function and if caching is enabled, put the return value in
        instance.__dict__ so that further attribute access on the instance
        returns the cached value instead of calling cached_property.__get__().
        """
        if instance is None:
            return self
        if cache_state:
            res = instance.__dict__[self.name] = self.func(instance)
        else:
            res = self.func(instance)
        return res


def conditional_cache(user_function, /):
    """
    Conditional, simple lightweight unbounded cache.  Sometimes called "memoize".
    """
    return lru_cache(maxsize=None)(user_function) if cache_state else user_function


def conditional_lru_cache(*args: Any, **kwargs: Any) -> Callable:
    """
    Applies the lru_cache decorator conditionally based on the cache state.

    """
    if not cache_state:
        kwargs["maxsize"] = 0
    return lru_cache(*args, **kwargs)
