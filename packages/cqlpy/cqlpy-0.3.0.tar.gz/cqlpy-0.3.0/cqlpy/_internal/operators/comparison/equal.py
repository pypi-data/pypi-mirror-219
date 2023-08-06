from cqlpy._internal.types.boolean import Boolean


def equal(left, right) -> Boolean:
    """
    Returns true if the left and right arguments are equal, false
    otherwise.

    You may also use the `==` operator to compare two values, though the
    result will be a Python type.

    [Specification](http://cql.hl7.org/09-b-cqlreference.html#equal)

    ## Parameters

    - `left`: The left argument.
    - `right`: The right argument.

    ## Returns

    True if the left and right arguments are equal, false otherwise.

    ## Usage

    ```python
    equal(Integer(1), Integer(1))  # True
    equal(Integer(1), Integer(2))  # False
    ```
    """
    return Boolean(left == right)
