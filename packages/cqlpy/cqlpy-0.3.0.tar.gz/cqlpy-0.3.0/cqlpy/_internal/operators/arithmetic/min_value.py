from cqlpy._internal.types.datetime import DateTime
from cqlpy._internal.types.null import Null, Some


def min_value(type_name: str) -> Some:
    """
    Returns the minimum value for the given type. Implements CQL's `minimum`.
    This is only defined for `DateTime`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#minimum)

    ## Parameters

    - `type_name`: The name of the `CqlAny` type to get the minimum value for.

    ## Returns

    The minimum value for the given type.

    ## Examples

    ```python
    min_value("DateTime")  # DateTime(1, 1, 1, 0, 0, 0, 0)
    ```
    """
    if type_name == "DateTime":
        return DateTime(1, 1, 1, 0, 0, 0, 0)
    else:
        return Null()
