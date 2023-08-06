from abc import ABCMeta, abstractmethod
from typing import Generic, Optional, Type, TypeVar


_FhirJsonType = TypeVar("_FhirJsonType", bound=object)
_CqlAnyType = TypeVar("_CqlAnyType")


class CqlAny(Generic[_FhirJsonType, _CqlAnyType], metaclass=ABCMeta):
    """
    All CQL types inherit from the CqlAny base class. This class cannot be instantiated.

    [Specification](http://cql.hl7.org/N1/09-b-cqlreference.html#any)
    """

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r})"

    def __bool__(self) -> bool:
        return bool(self.value)

    def __lt__(self, other: object) -> bool:
        if isinstance(other, CqlAny):
            return self.value < other.value

        if (
            isinstance(other, type(self.value))
            and hasattr(other, "__lt__")
            and hasattr(self.value, "__lt__")
        ):
            return self.value < other

        return False

    def __le__(self, other: object) -> bool:
        if isinstance(other, CqlAny):
            return self.value <= other.value

        if (
            isinstance(other, type(self.value))
            and hasattr(other, "__le__")
            and hasattr(self.value, "__le__")
        ):
            return self.value <= other

        return False

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CqlAny):
            return self.value == other.value

        if isinstance(other, type(self.value)):
            return self.value == other

        return False

    @property
    @abstractmethod
    def value(self) -> _CqlAnyType:
        """
        A representation of the CQL type as a python type that is useful for comparison operations.
        """
        pass

    @classmethod
    @abstractmethod
    def parse_fhir_json(
        self,
        fhir_json: _FhirJsonType,
        subtype: Optional[Type["CqlAny"]] = None,
    ) -> "CqlAny":
        """
        Instatiates the instance with the appropriate state based on snippet of FHIR.

        ## Parameters

        - `fhir_json`: A snippet of FHIR. The type of this parameter is determined by the type of the CqlAny instance, but is usually a `dict`.
        - `subtype`: The `CqlAny` child type for generic types. If this is not provided, the type will be inferred from the snippet.

        ## Usage

        ```python
        String.parse_fhir_json("foo")
        Code.parse_fhir_json({"code": "foo", "system": "bar"})
        List.parse_fhir_json(["1", "2", "3"], subtype=String)
        ```

        ## Returns

        A new instance of the `CqlAny` type.
        """
        pass

    @classmethod
    @abstractmethod
    def parse_cql(
        self,
        cql: str,
        subtype: Optional[Type["CqlAny"]] = None,
    ) -> "CqlAny":
        """
        Instatiates the instance with the appropriate state based on snippet of CQL represented as a string.

        ## Parameters

        - `cql`: The snippet of CQL to parse.
        - `subtype`: The `CqlAny` child type for generic types. If this is not provided, the type will be inferred from the snippet.

        ## Usage

        ```python
        String.parse_cql("foo")
        Integer.parse_cql("1")
        List.parse_cql("{1, 2, 3}", subtype=Integer)
        ```

        ## Returns

        A new instance of the `CqlAny` type.
        """
        pass
