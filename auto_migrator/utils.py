from typing import TypeVar, Callable, List

T = TypeVar('T')


def find(items: List[T], predicate: Callable[[T], bool]) -> [T or None]:
    for item in items:
        if predicate(item):
            return item

    return None
