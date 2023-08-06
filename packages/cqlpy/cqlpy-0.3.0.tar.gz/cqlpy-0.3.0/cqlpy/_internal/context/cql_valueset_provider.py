from typing import Union

from cqlpy._internal.exceptions import CqlPyValueError, ValuesetProviderError
from cqlpy._internal.logger import get_logger
from cqlpy._internal.types.valueset import Valueset
from cqlpy._internal.types.valueset_scope import ValuesetScope
from cqlpy._internal.providers.valueset_provider import (
    ValuesetProvider,
    ValuesetScopeProvider,
)

_COMMON_URL_PREFIXES = [
    "http://cts.nlm.nih.gov/fhir/ValueSet/",
    "http://hl7.org/fhir/ValueSet/",
]


def _clean_name(name: str) -> str:
    for prefix in _COMMON_URL_PREFIXES:
        if name.startswith(prefix):
            return name[len(prefix) :]
    return name


class CqlValuesetProvider:
    def __init__(self, valueset_provider: ValuesetProvider) -> None:
        self._valueset_provider = valueset_provider
        self.__logger = get_logger().getChild(self.__class__.__name__)

    def __get_valueset(self, item: Valueset) -> Valueset:
        if item.id is None:
            raise CqlPyValueError("value set id must be specified")

        name = _clean_name(item.id)
        result = self._valueset_provider.get_valueset(name=name, scope=None)

        if result:
            return Valueset.parse_fhir_json(result)

        self.__logger.warn(f"value set 'scopeless:{item.name}' not found")

        return item

    def __get_valueset_scope(self, item: ValuesetScope) -> list[Valueset]:
        if not isinstance(self._valueset_provider, ValuesetScopeProvider):
            raise ValuesetProviderError(
                "The value set provider does not support scope-based value set retrieval"
            )

        if item.id is None:
            raise CqlPyValueError("value set scope id must be specified")

        result = self._valueset_provider.get_valuesets_in_scope(scope=item.id)

        if result:
            return [
                Valueset.parse_fhir_json(valueset["resource"]) for valueset in result
            ]

        self.__logger.error(f"value set scope '{item.id}' not found")

        return []

    def __getitem__(
        self, item: Union[Valueset, ValuesetScope]
    ) -> Union[Valueset, list[Valueset]]:
        if isinstance(item, ValuesetScope):
            return self.__get_valueset_scope(item)
        return self.__get_valueset(item)
