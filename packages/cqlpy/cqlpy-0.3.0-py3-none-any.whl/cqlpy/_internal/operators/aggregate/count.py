from cqlpy._internal.types.integer import Integer


def count(argument: list) -> Integer:
    """
    Returns the number of elements in the given list.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#count)

    ## Parameters

    - `argument`: The list to get the number of elements of.

    ## Returns

    The number of elements in the given list.

    ## Usage

    ```python
    count([1, 2, 3])  # 3
    ```
    """
    return Integer(len(argument))
