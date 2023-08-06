from typing import Union, Optional, Type

from cqlpy._internal.types.any import CqlAny


class Integer(CqlAny[Union[str, int], int], int):
    """
    Represents a CQL integer.

    [Specification](http://cql.hl7.org/09-b-cqlreference.html#integer-1)
    """

    def __init__(self, value: Union[str, int]):
        """
        Creates a new Integer.

        ## Parameters

        - `value`: The value of the Integer.
        """
        self.__value = int(value)

    @property
    def value(self) -> int:
        return self.__value

    def __int__(self) -> int:
        return self.value

    def __new__(cls, value: Union[str, int]):
        return int.__new__(cls, value)

    @classmethod
    def parse_fhir_json(
        cls,
        fhir_json: Union[str, int],
        subtype: Optional[Type["CqlAny"]] = None,
    ) -> "Integer":
        return cls(fhir_json)

    @classmethod
    def parse_cql(cls, cql: str, subtype: Optional[Type[CqlAny]] = None) -> "Integer":
        return cls(cql)
