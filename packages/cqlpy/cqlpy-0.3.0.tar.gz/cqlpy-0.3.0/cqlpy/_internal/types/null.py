from typing import Optional, Type, TypeVar, Union

from cqlpy._internal.types.any import CqlAny


class Null(CqlAny[object, None]):
    """
    Represents the CQL Null value.
    """

    def __eq__(self, compare: object) -> bool:
        return compare == Null

    def __getitem__(self, query: str) -> "Null":
        return Null()

    def __iter__(self):
        return iter([])

    def __repr__(self) -> str:
        return "Null"

    def __str__(self) -> str:
        return "Null"

    @property
    def value(self) -> None:
        return None

    @classmethod
    def parse_cql(self, cql: str, subtype: Union[type[CqlAny], None] = None) -> CqlAny:
        return Null()

    @classmethod
    def parse_fhir_json(
        self,
        fhir_json: object,
        subtype: Union[type[CqlAny], None] = None,
    ) -> CqlAny:
        return Null()


_SomeType = TypeVar("_SomeType")
Some = Union[_SomeType, Null]
