# 8.14 Same Or Before https://cql.hl7.org/09-b-cqlreference.html#same-or-before-1


from cqlpy._internal.operators.nullological.is_null import is_null
from cqlpy._internal.types.datetime import DateTime

from cqlpy._internal.types.boolean import Boolean


def same_or_before(left: DateTime, right: DateTime) -> Boolean:
    """
    Returns true if the first `DateTime` is the same or before the second `DateTime`, false otherwise.
    Implements CQL's `same_or_before`.

    You may also use the `<=` operator to compare `DateTime`s, but the result will be a Python type.

    If either argument is `Null`, the result is `Null`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#same-or-before-1)

    ## Parameters

    - `left`: The first `DateTime`.
    - `right`: The second `DateTime`.

    ## Returns

    True if the first `DateTime` is the same or before the second `DateTime`, false otherwise.

    ## Usage

    ```python
    same_or_before(DateTime(2012, 1, 1), DateTime(2013, 1, 1))  # True
    ```
    """
    if is_null(left) or is_null(right):
        return Boolean(False)
    else:
        return Boolean(left.value <= right.value)
