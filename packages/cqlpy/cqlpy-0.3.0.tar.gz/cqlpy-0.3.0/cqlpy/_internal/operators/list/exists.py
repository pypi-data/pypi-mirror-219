# 10.6 Exists https://cql.hl7.org/09-b-cqlreference.html#exists


from cqlpy._internal.operators.nullological.is_null import is_null
from cqlpy._internal.types.boolean import Boolean


def exists(argument: list) -> Boolean:
    """
    Returns true if the given list is not null and has at least one element, false otherwise.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#exists)

    ## Parameters

    - `argument`: The list to check.

    ## Returns

    True if the given list is not null and has at least one element, false otherwise.

    ## Usage

    ```python
    exists([1, 2, 3])  # True
    ```
    """
    if is_null(argument):
        return Boolean(False)
    return Boolean(len(argument) > 0)
