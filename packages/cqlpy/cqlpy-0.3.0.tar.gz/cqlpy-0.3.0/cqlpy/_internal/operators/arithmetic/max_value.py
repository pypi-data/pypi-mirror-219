from cqlpy._internal.types.datetime import DateTime
from cqlpy._internal.types.null import Null, Some


def max_value(type_name: str) -> Some[DateTime]:
    """
    Returns the maximum value for the given type. Implements CQL's `maximum`.
    This is only defined for `DateTime`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#maximum)

    ## Parameters

    - `type_name`: The name of the `CqlAny` type to get the maximum value for.

    ## Returns

    The maximum value for the given type.

    ## Examples

    ```python
    max_value("DateTime")  # DateTime(9999, 12, 31, 23, 59, 59, 999)
    ```
    """
    if type_name == "DateTime":
        return DateTime(9999, 12, 31, 23, 59, 59, 999)
    else:
        return Null()
