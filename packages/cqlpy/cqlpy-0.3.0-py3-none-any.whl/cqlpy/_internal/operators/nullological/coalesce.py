from cqlpy._internal.operators.nullological.is_null import is_null

from cqlpy._internal.types.any import CqlAny
from cqlpy._internal.types.null import Null, Some


def coalesce(*args: Some[CqlAny]) -> Some[CqlAny]:
    """
    Returns the first non-null argument, or null if all arguments are null.

    [Specification](http://cql.hl7.org/09-b-cqlreference.html#coalesce)

    ## Parameters

    - `*args`: The arguments to coalesce.

    ## Returns

    The first non-null argument, or null if all arguments are null.

    ## Usage

    ```python
    coalesce(Integer(1), Integer(2), Integer(3))  # Integer(1)
    coalesce(None, Null(), Integer(3))  # Integer(3)
    coalesce(None, Null())  # Null()
    ```

    """
    for arg in args:
        if not is_null(arg):
            assert arg is not None
            return arg
    return Null()
