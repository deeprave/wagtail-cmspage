"""
This module implements conditional versions of lru_cache and Django's cached_property
decorators. The conditional versions allow the cache to be disabled by setting a flag
that is useful for testing.
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
    The cache can be disabled.

    A cached property can be made out of an existing method:
    (e.g. ``url = conditional_cached_property(get_absolute_url)``).
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
    Checks cache_state at runtime, not at decoration time.
    """
    def decorator(func):
        # Create both cached and uncached versions
        cached_func = lru_cache(*args, **kwargs)(func)
        uncached_func = func

        def wrapper(*func_args, **func_kwargs):
            if cache_state:
                return cached_func(*func_args, **func_kwargs)
            else:
                return uncached_func(*func_args, **func_kwargs)

        # Add cache_clear method for compatibility
        wrapper.cache_clear = getattr(cached_func, "cache_clear", lambda: None)
        wrapper.cache_info = getattr(cached_func, "cache_info", lambda: None)

        return wrapper

    # Handle both @conditional_lru_cache and @conditional_lru_cache() usage
    if len(args) == 1 and callable(args[0]) and not kwargs:
        # Called as @conditional_lru_cache
        func = args[0]
        return conditional_lru_cache()(func)
    else:
        # Called as @conditional_lru_cache() or @conditional_lru_cache(maxsize=...)
        return decorator
