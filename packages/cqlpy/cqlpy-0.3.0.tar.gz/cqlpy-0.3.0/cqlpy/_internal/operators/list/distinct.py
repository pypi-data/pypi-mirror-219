# 10.2 Distinct https://cql.hl7.org/09-b-cqlreference.html#distinct

from typing import TypeVar


_DistinctType = TypeVar("_DistinctType", bound=object)


def distinct(argument: list[_DistinctType]) -> list[_DistinctType]:
    """
    Returns a list containing only the distinct elements of the given list.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#distinct)

    ## Parameters

    - `argument`: The list to get the distinct elements of.

    ## Returns

    A list containing only the distinct elements of the given list.

    ## Usage

    ```python
    distinct([1, 2, 3, 2, 1])  # [1, 2, 3]
    ```
    """
    result = []
    for item in argument:
        if not (item in result):
            result.append(item)
    return result
