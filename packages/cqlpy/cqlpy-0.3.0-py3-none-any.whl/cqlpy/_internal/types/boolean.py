from typing import Optional, Type, Union
from cqlpy._internal.exceptions import CqlParseError
from cqlpy._internal.types.any import CqlAny


class Boolean(CqlAny[str, bool], int):
    """
    Represents the CQL Boolean type.

    [Specification](http://cql.hl7.org/N1/09-b-cqlreference.html#boolean-1)
    """

    def __init__(self, value: Union[bool, "Boolean"]):
        """
        Creates a new Boolean.

        ## Parameters

        - `value`: The value of the Boolean.
        """
        if isinstance(value, Boolean):
            self.__value = value.value
        else:
            self.__value = value

    @property
    def value(self) -> bool:
        return self.__value

    def __int__(self) -> int:
        return int(self.value)

    @classmethod
    def parse_fhir_json(
        cls,
        fhir_json: str,
        subtype: Optional[Type["CqlAny"]] = None,
    ) -> "Boolean":
        return cls(
            str(fhir_json).lower().replace('"', "").replace("'", "").strip() == "true"
        )

    @classmethod
    def parse_cql(cls, cql: str, subtype: Optional[Type[CqlAny]] = None) -> "Boolean":
        cql = cql.lower().replace('"', "").replace("'", "").strip()
        if cql == "true":
            return cls(True)
        if cql == "false":
            return cls(False)
        raise CqlParseError(f"Invalid CQL for Boolean: {cql}")
