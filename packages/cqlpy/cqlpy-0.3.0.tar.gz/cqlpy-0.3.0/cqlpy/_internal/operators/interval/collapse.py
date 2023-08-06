from typing import Optional
from cqlpy._internal.exceptions import CqlPyTypeError, CqlPyValueError
from cqlpy._internal.operators.nullological.is_null import is_null
from cqlpy._internal.types.date import Date
from cqlpy._internal.types.datetime import DateTime
from cqlpy._internal.types.decimal import Decimal
from cqlpy._internal.types.integer import Integer
from cqlpy._internal.types.list import List
from cqlpy._internal.types.interval import Interval, IntervalBoundType
from cqlpy._internal.types.null import Some, Null


def _get_sortable_interval_value(
    interval: Interval[IntervalBoundType],
) -> tuple[IntervalBoundType, int, IntervalBoundType, int]:
    low = interval.low if interval.low is not None else None
    high = interval.high if interval.high is not None else None
    if low is None or high is None:
        raise CqlPyValueError("Cannot sort interval with null bounds")
    return (
        low,
        0 if interval.low_closed else 1,
        high,
        0 if interval.high_closed else 1,
    )


def _space_between_points(
    first: IntervalBoundType,
    first_closed: Optional[bool],
    next_: IntervalBoundType,
    next_closed: Optional[bool],
) -> bool:
    some_first_closed = True if first_closed is None else first_closed
    some_next_closed = True if next_closed is None else next_closed

    if first == next_:
        return not (some_first_closed or some_next_closed)
    return first < next_


def collapse(
    argument: Some[List[Some[Interval[IntervalBoundType]]]],
) -> Some[List[Interval[IntervalBoundType]]]:
    """
    Collapses a list of intervals into a list of intervals with no overlaps.
    Implements CQL's `collapse`.

    If the argument is `Null`, the result is `Null`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#collapse)

    ## Parameters

    - `argument`: The list of intervals to collapse.

    ## Returns

    A new list of intervals with no overlaps.

    ## Usage

    ```python
    collapse(List([Interval(1, 2), Interval(2, 3)]))  # List([Interval(1, 3)])
    ```
    """

    if is_null(argument):
        return Null()
    assert isinstance(argument, List)
    if len(argument) == 0:
        return List([])
    if len(argument) == 1 and is_null(argument[0]):
        return List([])
    if len(argument) == 1:
        assert isinstance(argument[0], Interval)
        return List([argument[0]])

    sorted_list = sorted(
        [item for item in argument.value if not isinstance(item, Null)],
        key=_get_sortable_interval_value,
    )
    collapsed_list = [sorted_list[0]]

    for interval in sorted_list[1:]:
        last_interval = collapsed_list[-1]
        assert isinstance(interval, Interval)
        assert isinstance(last_interval, Interval)

        if is_null(interval):
            continue
        if (
            interval.low is None
            or last_interval.high is None
            or interval.high is None
            or last_interval.low is None
        ):
            raise CqlPyValueError("Cannot collapse interval with null bounds")

        if _space_between_points(
            first=last_interval.high,
            first_closed=last_interval.high_closed,
            next_=interval.low,
            next_closed=interval.low_closed,
        ):
            collapsed_list.append(interval)
            continue

        if last_interval.high == interval.high:
            high = last_interval.high
            high_closed = interval.high_closed or last_interval.high_closed
        elif last_interval.high > interval.high:
            high = last_interval.high
            high_closed = last_interval.high_closed
        else:
            high = interval.high
            high_closed = interval.high_closed

        if not isinstance(high, (DateTime, Date, Integer, Decimal)):
            raise CqlPyTypeError(f"Expected an interval type, got {type(high)}")
        if not isinstance(last_interval.low, (DateTime, Date, Integer, Decimal)):
            raise CqlPyTypeError(
                f"Expected an interval type, got {type(last_interval.low)}"
            )
        collapsed_list[-1] = Interval(
            last_interval.low,
            last_interval.low_closed if last_interval.low_closed is not None else True,
            high,
            high_closed if high_closed is not None else True,
        )

    return List([item for item in collapsed_list if not isinstance(item, Null)])
