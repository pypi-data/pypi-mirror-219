from typing import TypeVar

from cqlpy._internal.operators.nullological.is_null import is_null
from cqlpy._internal.types.null import Null, Some

_LastType = TypeVar("_LastType")


def last(argument: list[_LastType]) -> Some[_LastType]:
    """
    Returns the last element of the given list.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#last)

    ## Parameters

    - `argument`: The list to get the last element of.

    ## Returns

    The last element of the given list.

    ## Usage

    ```python
    last([1, 2, 3])  # 3
    ```
    """
    if is_null(argument):
        return Null()
    if len(argument) == 0:
        return Null()
    return argument[-1]
