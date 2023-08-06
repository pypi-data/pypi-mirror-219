from cqlpy._internal.types.boolean import Boolean


def is_false(argument: object) -> Boolean:
    """
    Returns True if the argument is False, False otherwise.

    [Specification](http://cql.hl7.org/09-b-cqlreference.html#isfalse)

    ## Parameters

    - `argument`: The item to check for falsity.

    ## Returns

    True if the argument is False, False otherwise.

    ## Usage

    ```python
    is_false(False)  # True
    is_false(Boolean(True))  # False
    ```
    """
    return Boolean(
        (argument == False) or (hasattr(argument, "value") and argument.value == False)
    )
