from typing import TypeVar, Union

from cqlpy._internal.exceptions import CqlPyValueError
from cqlpy._internal.operators.comparison.in_list import in_list
from cqlpy._internal.operators.interval.in_interval import in_interval
from cqlpy._internal.operators.nullological.is_null import is_null
from cqlpy._internal.types.boolean import Boolean
from cqlpy._internal.types.date import Date
from cqlpy._internal.types.datetime import DateTime
from cqlpy._internal.types.decimal import Decimal
from cqlpy._internal.types.integer import Integer
from cqlpy._internal.types.interval import Interval
from cqlpy._internal.types.null import Null, Some

_InType = TypeVar("_InType")
_ArgumentType = Some[Union[list[Some[_InType]], Interval]]


def cql_in(item: Some[_InType], argument: _ArgumentType) -> Boolean:
    """
    Combines list and interval `in` operators into one function.

    Returns `True` if the given item is in the given list or interval, `False` otherwise.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#in)

    ## Parameters

    - `item`: The item to check for.
    - `argument`: The list or interval to check.

    ## Returns

    True if the given item is in the given list or interval, false otherwise.

    ## Usage

    ```python
    cql_in(1, [1, 2, 3])  # True
    ```
    """
    if is_null(item) or is_null(argument):
        return Boolean(False)
    assert not isinstance(item, Null)
    assert not isinstance(argument, Null)

    if isinstance(argument, Interval):
        if (
            not isinstance(item, Date)
            and not isinstance(item, DateTime)
            and not isinstance(item, Integer)
            and not isinstance(item, Decimal)
        ):
            raise CqlPyValueError("Item must be a supported interval comparison type")
        return Boolean(in_interval(item, argument))
    return Boolean(in_list(item, argument))
