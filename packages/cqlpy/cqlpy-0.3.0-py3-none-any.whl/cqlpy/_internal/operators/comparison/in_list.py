from typing import TypeVar

from cqlpy._internal.types.boolean import Boolean
from cqlpy._internal.types.code import Code

_InListType = TypeVar("_InListType")


def in_list(element: _InListType, argument: list[_InListType]) -> Boolean:
    """
    Returns true if the given element is in the given list, false otherwise.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#in-1)

    ## Parameters

    - `element`: The element to check for.
    - `argument`: The list to check.

    ## Returns

    True if the given element is in the given list, false otherwise.

    ## Usage

    ```python
    in_list(1, [1, 2, 3])  # True
    ```
    """
    for item in argument:
        if (
            isinstance(element, Code)
            and isinstance(item, Code)
            and element.code == item.code
        ):
            return Boolean(True)
        if element == item:
            return Boolean(True)

    return Boolean(False)
