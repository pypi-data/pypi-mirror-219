from cqlpy._internal.operators.interval.included_in import included_in
from cqlpy._internal.operators.nullological.is_null import is_null
from cqlpy._internal.types.boolean import Boolean
from cqlpy._internal.types.interval import Interval


def overlaps(left: Interval, right: Interval) -> Boolean:
    """
    Returns true if the first `Interval` has any point included in the second `Interval`, false otherwise.
    Implements CQL's `overlaps`.

    If either argument is `Null`, the result is `Null`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#overlaps)

    ## Parameters

    - `left`: The first `Interval`.
    - `right`: The second `Interval`.

    ## Returns

    True if the first `Interval` has any point included in the second `Interval`, false otherwise.

    ## Usage

    ```python
    overlaps(Interval(1, 3), Interval(2, 3))  # True
    ```
    """
    if is_null(left) or is_null(right):
        return Boolean(False)

    if included_in(left, right) or included_in(right, left):
        return Boolean(True)

    if included_in(left.low, right) or included_in(left.high, right):
        return Boolean(True)

    return Boolean(False)
