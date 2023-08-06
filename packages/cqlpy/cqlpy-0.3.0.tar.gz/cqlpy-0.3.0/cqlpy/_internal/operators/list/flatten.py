# 10.7 Flatten https://cql.hl7.org/09-b-cqlreference.html#flatten

from typing import TypeVar


_FlattenType = TypeVar("_FlattenType")


def flatten(argument: list[list[_FlattenType]]) -> list[_FlattenType]:
    """
    Returns a single list from the given list of lists. The elements of the result are the elements of the lists in the given list, in order.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#flatten)

    ## Parameters

    - `argument`: The list of lists to flatten.

    ## Returns

    A single list from the given list of lists.

    ## Usage

    ```python
    flatten([[1, 2], [3, 4]])  # [1, 2, 3, 4]
    ```
    """
    result = []
    for item in argument:
        result += item
    return result
