from typing import Generic, Optional, Type, TypeVar, Union, Any

from cqlpy._internal.types.any import CqlAny
from cqlpy._internal.types.date import Date
from cqlpy._internal.types.datetime import DateTime
from cqlpy._internal.types.decimal import Decimal
from cqlpy._internal.types.integer import Integer

from cqlpy._internal.exceptions import CqlPyValueError


IntervalBoundType = TypeVar(
    "IntervalBoundType", bound=Union[DateTime, Date, Integer, Decimal]
)


def _infer_generic_value(value: str) -> Union[DateTime, Date, Integer, Decimal]:
    if len(value) <= 10:
        try:
            return Date.parse_cql(value)
        except ValueError:
            pass
    try:
        DateTime.parse_cql(value)
    except ValueError:
        pass

    try:
        return Integer(value)
    except ValueError:
        pass

    try:
        return Decimal(value)
    except ValueError:
        pass

    raise CqlPyValueError(f"Could not infer type for {value}")


class Interval(
    Generic[IntervalBoundType],
    CqlAny[
        dict[str, Any],
        tuple[
            Optional[IntervalBoundType],
            Optional[bool],
            Optional[IntervalBoundType],
            Optional[bool],
        ],
    ],
):
    """
    Specifies a range of values. The bounds of the interval may be open or closed.
    The bounds of the interval must be the same type and may be one of `DateTime`, `Date`, `Integer`, or `Decimal`.
    """

    def __init__(
        self,
        low: Optional[IntervalBoundType] = None,
        low_closed: Optional[bool] = None,
        high: Optional[IntervalBoundType] = None,
        high_closed: Optional[bool] = None,
    ):
        """
        Creates a new `Interval` with the specified bounds.

        ## Parameters

        - `low`: The lower bound of the interval.
        - `low_closed`: Whether the lower bound is closed.
        - `high`: The upper bound of the interval.
        - `high_closed`: Whether the upper bound is closed.

        ## Usage

        ```python
        Interval(1, True, 10, False)
        ```
        """
        self.low = low
        self.low_closed = low_closed
        self.high = high
        self.high_closed = high_closed

    def __str__(self) -> str:
        return (
            ("[" if self.low_closed else "(")
            + str(self.low)
            + ", "
            + str(self.high)
            + ("]" if self.high_closed else ")")
        )

    @property
    def value(
        self,
    ) -> tuple[
        Optional[IntervalBoundType],
        Optional[bool],
        Optional[IntervalBoundType],
        Optional[bool],
    ]:
        return self.low, self.low_closed, self.high, self.high_closed

    @classmethod
    def parse_cql(cls, cql: str, subtype: Optional[Type[CqlAny]] = None) -> "Interval":
        if not cql:
            return cls()

        cql = cql.replace("Interval", "")

        low_value = cql.split(",")[0][1:]
        high_value = cql.split(",")[1][:-1]

        if subtype in (Date, DateTime, Integer, Decimal):
            low = subtype.parse_cql(low_value)
            high = subtype.parse_cql(high_value)
        else:
            low = _infer_generic_value(low_value)
            high = _infer_generic_value(high_value)

        low_closed = cql[:1] == "["
        high_closed = cql[-1] == "]"

        return cls(
            low=low,  # type: ignore  # Inferred generics have unclear usage.
            low_closed=low_closed,
            high=high,  # type: ignore  # Inferred generics have unclear usage.
            high_closed=high_closed,
        )

    @classmethod
    def parse_fhir_json(
        cls,
        fhir_json: dict[str, Any],
        subtype: Optional[Type["CqlAny"]] = None,
    ) -> "Interval":
        low_value = fhir_json["start"]
        if subtype in (Date, DateTime, Integer, Decimal):
            low = subtype.parse_fhir_json(low_value)
        else:
            low = _infer_generic_value(str(low_value))

        if "end" in fhir_json:
            high_value = fhir_json["end"]
            if subtype in (Date, DateTime, Integer, Decimal):
                high = subtype.parse_fhir_json(str(high_value))
            else:
                high = _infer_generic_value(str(high_value))
        else:
            high = low

        low_closed = True
        high_closed = True

        return cls(
            low=low,  # type: ignore  # Inferred generics have unclear usage.
            low_closed=low_closed,
            high=high,  # type: ignore  # Inferred generics have unclear usage.
            high_closed=high_closed,
        )
