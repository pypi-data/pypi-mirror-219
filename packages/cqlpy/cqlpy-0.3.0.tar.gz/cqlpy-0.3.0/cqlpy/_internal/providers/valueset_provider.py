from typing import Any, Optional, Protocol, runtime_checkable


@runtime_checkable
class ValuesetProvider(Protocol):
    """
    A protocol describing the interface for a value set provider. A value set provider
    is responsible for retrieving value sets from a value set repository.
    """

    def get_valueset(self, name: str, scope: Optional[str]) -> dict[str, Any]:
        """
        Retrieves a value set from the value set repository.

        ## Parameters

        - `name`: The name of the value set to retrieve. This should be unique within
            the scope of the value set provider.
        - `scope`: The scope of the value set to retrieve. If the value set provider
            does not support scoping, this parameter should be ignored.

        ## Returns

        The value set definition as a dictionary.
        """
        ...


@runtime_checkable
class ValuesetScopeProvider(ValuesetProvider, Protocol):
    """
    A protocol describing the interface for a value set provider that supports scoping
    value sets. A value set provider is responsible for retrieving value sets from a
    value set repository.
    """

    def get_valuesets_in_scope(self, scope: str) -> list[dict[str, Any]]:
        """
        Retrieves all value sets in the specified scope from the value set repository.

        ## Parameters

        - `scope`: The scope of the value sets to retrieve.

        ## Returns

        A list of value set definitions as dictionaries.
        """
        ...
