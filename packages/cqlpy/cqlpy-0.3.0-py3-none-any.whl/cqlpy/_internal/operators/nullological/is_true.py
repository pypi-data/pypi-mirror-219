from cqlpy._internal.types.boolean import Boolean


def is_true(argument: object) -> Boolean:
    """
    Returns True if the argument is True, False otherwise.

    [Specification](http://cql.hl7.org/09-b-cqlreference.html#istrue)

    ## Parameters

    - `argument`: The item to check for truth.

    ## Returns

    True if the argument is True, False otherwise.

    ## Usage

    ```python
    is_true(True)  # True
    is_true(Boolean(False))  # False
    ```
    """
    return Boolean(
        (argument == True) or (hasattr(argument, "value") and argument.value == True)
    )
