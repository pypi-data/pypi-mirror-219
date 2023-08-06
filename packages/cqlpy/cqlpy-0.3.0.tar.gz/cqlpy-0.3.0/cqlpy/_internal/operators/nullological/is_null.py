from cqlpy._internal.types.null import Null
from cqlpy._internal.types.boolean import Boolean


def is_null(argument: object) -> Boolean:
    """
    Returns true if the argument is null, false otherwise.

    [Specification](http://cql.hl7.org/09-b-cqlreference.html#isnull)

    ## Parameters

    - `argument`: The item to check for nullity.

    ## Returns

    True if the argument is null, False otherwise.

    ## Usage

    ```python
    is_null(None)  # True
    is_null(Null())  # True
    is_null(Integer(1))  # False
    ```
    """
    return Boolean(
        (argument is None)
        or (argument == Null)
        or (
            hasattr(argument, "value")
            and ((argument.value is None) or (argument.value == Null))
        )
    )
