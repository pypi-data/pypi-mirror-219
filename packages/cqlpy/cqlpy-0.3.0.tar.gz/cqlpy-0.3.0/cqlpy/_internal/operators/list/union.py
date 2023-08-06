from typing import TypeVar

from cqlpy._internal.operators.list.distinct import distinct


_UnionType = TypeVar("_UnionType")


def union(left: list[_UnionType], right: list[_UnionType]) -> list[_UnionType]:
    """
    Returns a list containing the elements of both the left and right
    lists with duplicates removed.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#union-1)

    ## Parameters

    - `left`: The left list.
    - `right`: The right list.

    ## Returns

    A list containing the elements of both the left and right lists.

    ## Usage

    ```python
    union([1, 2], [3, 4])  # [1, 2, 3, 4]
    ```
    """
    return distinct(left + right)
