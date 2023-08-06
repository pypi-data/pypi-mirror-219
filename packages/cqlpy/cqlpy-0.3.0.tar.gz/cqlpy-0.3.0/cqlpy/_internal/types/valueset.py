from typing import Any, Optional, Type
from cqlpy._internal.types.any import CqlAny
from cqlpy._internal.types.code import Code


class Valueset(CqlAny[dict[str, Any], list[Code]]):
    """
    Represents a CQL valueset. This is not a pointer, but rather a full enumeration of constituent `cqlpy.types.Code`s.

    [Specification](http://cql.hl7.org/09-b-cqlreference.html#valueset)
    """

    def __init__(
        self,
        valueset_id: Optional[str] = None,
        name: Optional[str] = None,
        version: Optional[str] = None,
        use_context: Optional[str] = None,
        codes: Optional[list[Code]] = None,
    ):
        """
        Creates a new Valueset.

        ## Parameters

        - `valueset_id`: The id of the Valueset. This should be unique in the context of a `cqlpy.providers.ValuesetProvider`.
        - `name`: The name of the Valueset.
        - `version`: The version of the Valueset. This is not considered in its uniqueness.
        - `use_context`: The use context of the Valueset.
        - `codes`: The `cqlpy.types.Code`s that make up the Valueset.
        """
        self.id = valueset_id
        self.name = name
        self.version = version
        self.use_context = use_context
        self.codes: list[Code] = codes or []

    def __str__(self) -> str:
        return (
            "id:"
            + (self.id or "")
            + ", version:"
            + (self.version or "")
            + ", codes:"
            + str([str(code) for code in self.codes])
        )

    @property
    def value(self) -> list[Code]:
        return self.codes

    @classmethod
    def parse_cql(cls, cql: str, subtype: Optional[Type[CqlAny]] = None) -> "Valueset":
        valueset_id = ""
        version = ""
        name = ""

        return cls(
            valueset_id=valueset_id,
            name=name,
            version=version,
        )

    @classmethod
    def parse_fhir_json(
        cls,
        fhir_json: dict[str, Any],
        subtype: Optional[Type["CqlAny"]] = None,
    ) -> "Valueset":
        version: str = fhir_json["version"]
        name: str = fhir_json["name"]
        includes: list[dict[str, Any]] = fhir_json["compose"]["include"]

        codes = [
            Code(
                system=include.get("system", ""),
                code=concept["code"],
                display=concept.get("display", ""),
                version=include.get("version", ""),
            )
            for include in includes
            for concept in include["concept"]
        ]

        return cls(
            valueset_id="",
            name=name,
            version=version,
            codes=codes,
        )
