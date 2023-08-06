from cqlpy._internal.types.boolean import Boolean
from cqlpy._internal.types.string import String


def ends_with(argument: String, suffix: String) -> Boolean:
    """
    Returns true if the argument ends with the given suffix, false otherwise.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#endswith)

    ## Parameters

    - `argument`: The string to check.
    - `suffix`: The suffix to check for.

    ## Returns

    True if the argument ends with the given suffix, false otherwise.

    ## Usage

    ```python
    ends_with(String("Hello, world!"), String("world!"))  # True
    ends_with(String("Hello, world!"), String("world"))  # False
    ```
    """

    return Boolean(argument[-len(suffix) :] == suffix)
