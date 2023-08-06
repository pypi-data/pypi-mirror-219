from typing import Optional, Type

from cqlpy._internal.types.any import CqlAny


class CodeSystem(CqlAny[object, tuple[Optional[str], Optional[str]]]):
    """
    A pointer to an externally-defined code system.

    [Specification](http://cql.hl7.org/N1/09-b-cqlreference.html#codesystem)
    """

    def __init__(
        self,
        id: Optional[str] = None,
        version: Optional[str] = None,
    ):
        """
        Creates a new CodeSystem.

        ## Parameters

        - `id`: The globally-unique id of the CodeSystem.
        - `version`: The version of the CodeSystem.
        """
        self.id = id
        self.version = version

    def __str__(self) -> str:
        return "id:" + str(self.id) + ", version:" + str(self.version)

    @property
    def value(self) -> tuple[Optional[str], Optional[str]]:
        return self.id, self.version

    @classmethod
    def parse_cql(
        cls, cql: str, subtype: Optional[Type[CqlAny]] = None
    ) -> "CodeSystem":
        return cls()

    @classmethod
    def parse_fhir_json(
        cls,
        fhir_json: object,
        subtype: Optional[Type["CqlAny"]] = None,
    ) -> "CodeSystem":
        return cls()
