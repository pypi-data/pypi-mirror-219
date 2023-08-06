# 9.13 Included In https://cql.hl7.org/09-b-cqlreference.html#included-in

from typing import Union
from cqlpy._internal.exceptions import CqlPyTypeError
from cqlpy._internal.operators.nullological.is_null import is_null
from cqlpy._internal.types.date import Date
from cqlpy._internal.types.datetime import DateTime
from cqlpy._internal.types.decimal import Decimal
from cqlpy._internal.types.integer import Integer

from cqlpy._internal.types.interval import Interval
from cqlpy._internal.types.null import Null

from cqlpy._internal.types.boolean import Boolean


_IncludedInType = Union[Interval, Date, DateTime, Integer, Decimal, None, Null]


def included_in(left: _IncludedInType, right: Interval) -> Boolean:
    """
    Returns `True` if the left argument is part of the right `Interval`, `False` otherwise. If either argument is `Null`, the result is `False`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#included-in)

    ## Parameters

    - `left`: The point or interval to check for inclusion.
    - `right`: The interval to check for inclusion in.

    ## Returns

    `True` if the left argument is part of the right `Interval`, `False` otherwise.

    ## Usage

    ```python
    included_in(1, Interval(0, 2))  # True
    included_in(Interval(1, 2), Interval(0, 2))  # True
    ```
    """
    if is_null(left) or is_null(right):
        return Boolean(False)

    if isinstance(left, Interval):
        if (
            len(
                {
                    left.low.__class__,
                    left.high.__class__,
                    right.low.__class__,
                    right.high.__class__,
                }
            )
            > 1
        ):
            raise CqlPyTypeError("Cannot compare intervals of different types")

        left_in = included_in(left.low, right)
        right_in = included_in(left.high, right)
        if is_null(left_in) or is_null(right_in):
            return Boolean(False)
        return Boolean(left_in.value and right_in.value)

    if (
        isinstance(left, DateTime)
        and isinstance(right, Interval)
        and isinstance(right.low, DateTime)
        and isinstance(right.high, DateTime)
    ):
        return Boolean(
            (
                (left > right.low)
                and (left < right.high)
                or (left == right.low and right.low_closed)
                or (left == right.high and right.high_closed)
            )
            or False
        )

    return Boolean(False)
