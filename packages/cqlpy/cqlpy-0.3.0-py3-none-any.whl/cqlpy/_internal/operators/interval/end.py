from cqlpy._internal.operators.nullological.is_null import is_null
from cqlpy._internal.types.datetime import DateTime
from cqlpy._internal.types.interval import Interval
from cqlpy._internal.types.null import Null, Some


def end(argument: Interval[DateTime]) -> Some[DateTime]:
    """
    Returns the end of the given `Interval`.

    If the argument is `Null`, the result is `Null`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#end)

    ## Parameters

    - `argument`: The `Interval` to get the end of.

    ## Returns

    The end of the given `Interval`.

    ## Usage

    ```python
    end(Interval(DateTime(2012, 1, 1), DateTime(2013, 1, 1)))  # DateTime(2013, 1, 1)
    ```
    """
    if not is_null(argument):
        return argument.high or Null()
    else:
        return Null()
