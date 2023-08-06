from typing import TypeVar

from cqlpy._internal.operators.nullological.is_null import is_null
from cqlpy._internal.types.null import Null, Some

_FirstType = TypeVar("_FirstType")


def first(argument: list[_FirstType]) -> Some[_FirstType]:
    """
    Returns the first element of the given list.

    If the argument is `Null` or empty, the result is `Null`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#first)

    ## Parameters

    - `argument`: The list to get the first element of.

    ## Returns

    The first element of the given list.

    ## Usage

    ```python
    first([1, 2, 3])  # 1
    ```
    """
    if is_null(argument):
        return Null()
    if len(argument) == 0:
        return Null()
    return argument[0]
