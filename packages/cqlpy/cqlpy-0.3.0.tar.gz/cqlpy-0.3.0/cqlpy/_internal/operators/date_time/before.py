from cqlpy._internal.operators.date_time.date_time_precision import DateTimePrecision
from cqlpy._internal.operators.nullological.is_null import is_null
from cqlpy._internal.types.boolean import Boolean
from cqlpy._internal.types.datetime import DateTime
from cqlpy._internal.types.null import Null, Some


def before(
    left: DateTime,
    right: DateTime,
    precision: DateTimePrecision = DateTimePrecision.Millisecond,
) -> Some[Boolean]:
    """
    Returns true if the first `DateTime` is before the second `DateTime`, false otherwise.
    Implements CQL's `before`.

    If either argument is `Null`, the result is `Null`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#before)

    ## Parameters

    - `left`: The first `DateTime`.
    - `right`: The second `DateTime`.
    - `precision`: The precision to compare the `DateTime`s at.

    ## Returns

    True if the first `DateTime` is before the second `DateTime`, false otherwise.

    ## Usage

    ```python
    before(DateTime(2012, 1, 1), DateTime(2013, 1, 1))  # True
    ```
    """
    if is_null(left) or is_null(right):
        return Null()
    else:
        return Boolean(left < right)
