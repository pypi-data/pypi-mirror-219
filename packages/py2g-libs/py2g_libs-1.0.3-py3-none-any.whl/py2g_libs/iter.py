from typing import Iterable, TypeVar

T = TypeVar('T')
def first_of_singleton(iterable: Iterable) -> T:
    value = next(iterable)
    assert next(iterable, None) == None, "Iterable cannot contain more than one element"
    return value
