# 8.15 Substract https://cql.hl7.org/09-b-cqlreference.html#subtract-1

from datetime import timedelta
from dateutil.relativedelta import relativedelta

from cqlpy._internal.operators.date_time.date_time_precision import DateTimePrecision
from cqlpy._internal.operators.nullological.is_null import is_null
from cqlpy._internal.types.datetime import DateTime
from cqlpy._internal.types.null import Null, Some
from cqlpy._internal.types.quantity import Quantity


def subtract(left: DateTime, right: Quantity) -> Some[DateTime]:
    """
    Subtracts the given quantity from the given `DateTime`. Implements CQL's `subtract`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#subtract-1)

    ## Parameters

    - `left`: The `DateTime` to subtract from.
    - `right`: The `Quantity` to subtract.

    ## Returns

    A new `DateTime` with the given quantity subtracted from it.

    ## Usage

    ```python
    subtract(DateTime(2012, 1, 1), Quantity(1, "years"))  # DateTime(2011, 1, 1)
    ```
    """
    if is_null(left) or is_null(right):
        return Null()
    assert right.value is not None

    if (right.unit == "days") or (right.unit == DateTimePrecision.Day):
        return DateTime().parse_datetime(left.value - timedelta(days=right.value))
    if (right.unit == "weeks") or (right.unit == DateTimePrecision.Week):
        return DateTime().parse_datetime(left.value - timedelta(days=7 * right.value))
    if (right.unit == "months") or (right.unit == DateTimePrecision.Month):
        months = int(right.value)
        return DateTime().parse_datetime(left.value - relativedelta(months=months))
    if (right.unit == "years") or (right.unit == DateTimePrecision.Year):
        years = int(right.value)
        return DateTime().parse_datetime(left.value - relativedelta(years=years))
    return Null()
