from typing import Union

from cqlpy._internal.types.date import Date
from cqlpy._internal.types.datetime import DateTime


def to_datetime(argument: Union[Date, DateTime]) -> DateTime:
    """
    Converts a Date to a DateTime. Note that Date is a subtype of DateTime,
    so this function is a no-op in CQLpy.

    [Specification](http://cql.hl7.org/09-b-cqlreference.html#todatetime)

    ## Parameters

    - `argument`: The `Date` to convert.

    ## Returns

    A `DateTime` with the same year, month, and day as the given `Date`.

    ## Usage

    ```python
    date = Date(year=2020, month=1, day=1)
    to_datetime(date)  # DateTime(year=2020, month=1, day=1)
    ```
    """
    return argument
