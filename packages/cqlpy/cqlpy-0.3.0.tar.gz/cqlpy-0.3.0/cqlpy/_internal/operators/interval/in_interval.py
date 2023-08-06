from typing import Union
from cqlpy._internal.exceptions import CqlPyValueError

from cqlpy._internal.operators.nullological.is_null import is_null
from cqlpy._internal.types.boolean import Boolean
from cqlpy._internal.types.date import Date
from cqlpy._internal.types.datetime import DateTime
from cqlpy._internal.types.decimal import Decimal
from cqlpy._internal.types.integer import Integer
from cqlpy._internal.types.interval import Interval
from cqlpy._internal.types.null import Null, Some

_InIntervalType = Union[Date, DateTime, Integer, Decimal, None]


def in_interval(point: Some[_InIntervalType], argument: Some[Interval]) -> Boolean:
    """
    Returns `True` if the given point is in the given interval, `False` otherwise.

    If the point or interval is `Null`, the result is `False`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#in)

    ## Parameters

    - `point`: The point to check.
    - `argument`: The interval to check.

    ## Returns

    `True` if the given point is in the given interval, `False` otherwise.

    ## Usage

    ```python
    in_interval(1, Interval(0, 2))  # True
    ```
    """
    if is_null(argument):
        return Boolean(False)
    if isinstance(point, Null):
        return Boolean(False)
    assert point is not None

    if not isinstance(argument, Interval):
        return Boolean(False)
    if is_null(argument.low) or is_null(argument.high):
        return Boolean(False)
    if isinstance(argument.low, Null) or isinstance(argument.high, Null):
        return Boolean(False)
    assert argument.low is not None
    assert argument.high is not None

    if len({point.__class__, argument.low.__class__, argument.high.__class__}) > 1:
        raise CqlPyValueError("point must be of the same type as the interval")

    return Boolean(
        (
            (point > argument.low)
            and (point < argument.high)
            or (point == argument.low and argument.low_closed)
            or (point == argument.high and argument.high_closed)
        )
        or False
    )
