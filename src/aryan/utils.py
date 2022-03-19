import inspect
from typing import Callable, Union, Optional, Iterable, get_origin, get_args
from functools import partial
import traceback


async def async_(obj):
    return (await obj) if inspect.isawaitable(obj) else obj


def get_event_from_func(function: Callable):
    from .event import Event
    if isinstance(function, partial):
        function = function.func
    if len(function.__annotations__) == 0:
        return None
    for value in function.__annotations__.values():
        if get_origin(value) is Union:
            if all(issubclass(i, Event) for i in get_args(value)):
                return get_args(value)
        elif get_origin(value) is Optional:
            pass
        elif isinstance(value, Iterable):
            return value
        elif issubclass(value, Event):
            return value
