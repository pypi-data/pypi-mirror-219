from dateutil.relativedelta import relativedelta

from cqlpy._internal.operators.date_time.date_time_precision import DateTimePrecision
from cqlpy._internal.operators.nullological.is_null import is_null
from cqlpy._internal.types.datetime import DateTime
from cqlpy._internal.types.integer import Integer
from cqlpy._internal.types.null import Null, Some


def difference_between(
    low: DateTime,
    high: DateTime,
    precision: DateTimePrecision,
) -> Some[Integer]:
    """
    Returns the number of boundaries crossed for the specified precision between the two `DateTime`s.
    Implements CQL's `difference between`.

    If either argument is `Null`, the result is `Null`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#difference)

    ## Parameters

    - `low`: The first `DateTime`.
    - `high`: The second `DateTime`.

    ## Returns

    The number of boundaries crossed between the two `DateTime`s.

    ## Usage

    ```python
    difference_between(DateTime(2012, 1, 1), DateTime(2013, 1, 1), DateTimePrecision.Year)  # Integer(1)
    ```
    """
    if is_null(low) or is_null(high):
        return Null()
    if precision == DateTimePrecision.Day:
        return Integer((high.value - low.value).days)
    if precision == DateTimePrecision.Month:
        return Integer(
            (high.value.year - low.value.year) * 12 + high.value.month - low.value.month
        )
    if precision == DateTimePrecision.Year:
        return Integer(relativedelta(high.value, low.value).years)

    return Null()
