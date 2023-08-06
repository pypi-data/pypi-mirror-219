from cqlpy._internal.types.any import CqlAny
from typing import Union, Optional, Type


class Decimal(CqlAny[Union[str, float, int], float], float):
    """
    Represents a CQL decimal.

    [Specification](http://cql.hl7.org/09-b-cqlreference.html#decimal-1)
    """

    def __init__(self, value: Union[str, float, int]):
        """
        Creates a new Decimal.

        ## Parameters

        - `value`: The value of the Decimal.
        """
        self.__value = float(value)

    def __repr__(self) -> str:
        return f"Decimal({self.value})"

    def __new__(cls, value: Union[str, float, int]):
        return float.__new__(cls, value)

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Decimal):
            return self.value == __value.value

        if isinstance(__value, (str, float, int)):
            return self.value == float(__value)

        return False

    @property
    def value(self) -> float:
        return self.__value

    @classmethod
    def parse_fhir_json(
        cls,
        fhir_json: Union[str, int, float],
        subtype: Optional[Type["CqlAny"]] = None,
    ) -> "Decimal":
        return cls(fhir_json)

    @classmethod
    def parse_cql(cls, cql: str, subtype: Optional[Type[CqlAny]] = None) -> "Decimal":
        return cls(cql)
