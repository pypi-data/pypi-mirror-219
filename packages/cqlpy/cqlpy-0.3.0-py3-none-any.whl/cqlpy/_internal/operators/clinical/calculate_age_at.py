from typing import Optional

from cqlpy._internal.operators.date_time.date_time_precision import DateTimePrecision
from cqlpy._internal.types.datetime import DateTime
from cqlpy._internal.types.integer import Integer


def calculate_age_at(
    birth_date: DateTime,
    as_of: DateTime,
    precision: Optional[DateTimePrecision] = None,
) -> Integer:
    """
    Calculates the age of the given `DateTime` at the given `DateTime`. Implements CQL's `calculateAgeAt`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#calculateageat)

    ## Parameters

    - `birth_date`: The `DateTime` to calculate the age of.
    - `as_of`: The `DateTime` to calculate the age at.
    - `precision`: The precision to calculate the age at.

    ## Returns

    The age of the given `DateTime` at the given `DateTime`.

    ## Usage

    ```python
    calculate_age_at(DateTime(2012, 1, 1), DateTime(2013, 1, 1))  # Integer(1)
    ```
    """
    return Integer(
        as_of.value.year
        - birth_date.value.year
        - (
            (as_of.value.month, as_of.value.day)
            < (birth_date.value.month, birth_date.value.day)
        )
    )
