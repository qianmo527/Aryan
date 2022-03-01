from typing import List, Callable

from . import Event


class Filter:
    conditions: List[Callable[[Event], bool]]

    def __init__(self, conditions=[]) -> None:
        self.conditions = conditions if isinstance(conditions, list) else [conditions]

    def filter(self, event: Event) -> bool:
        if all([func(event) for func in self.conditions]):
            return True
        return False

    def __add__(self, func: Callable[[Event], bool]):
        assert isinstance(func, Callable)
        _ = self.conditions.copy()
        _.append(func)
        return Filter(_)
