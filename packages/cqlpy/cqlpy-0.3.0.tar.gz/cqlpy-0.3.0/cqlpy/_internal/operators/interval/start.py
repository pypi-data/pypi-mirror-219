# 9.28 Start https://cql.hl7.org/09-b-cqlreference.html#start


from typing import Union
from cqlpy._internal.operators.nullological.is_null import is_null
from cqlpy._internal.types.any import CqlAny
from cqlpy._internal.types.date import Date
from cqlpy._internal.types.datetime import DateTime
from cqlpy._internal.types.decimal import Decimal
from cqlpy._internal.types.integer import Integer
from cqlpy._internal.types.interval import Interval
from cqlpy._internal.types.null import Null, Some


def start(argument: Interval[DateTime]) -> Some[DateTime]:
    """
    Returns the start of the given `Interval`.

    If the argument is `Null`, the result is `Null`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#start)

    ## Parameters

    - `argument`: The `Interval` to get the start of.

    ## Returns

    The start of the given `Interval`.

    ## Usage

    ```python
    start(Interval(1, 2))  # 1
    ```
    """
    if not is_null(argument):
        return argument.low or Null()
    else:
        return Null()
