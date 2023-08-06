from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional, Union

from cqlpy._internal.types.code import Code
from cqlpy._internal.types.valueset import Valueset

ResourceQueryFilter = Union[Valueset, list[Code], Code, list[Valueset]]


@dataclass(frozen=True, eq=True)
class ResourceQuery:
    resource_type: str = field()
    property_filter: Optional[ResourceQueryFilter] = field(default=None)
    property_name: Optional[str] = field(default=None)

    @classmethod
    def from_query(cls, query: Union[str, tuple[str, ResourceQueryFilter, str]]):
        if isinstance(query, tuple):
            resource_type = query[0]
            property_filter = query[1] if len(query) > 1 else None
            property_name = query[2] if len(query) > 1 else None

        else:
            resource_type = query
            property_filter = None
            property_name = None

        resource_type = (
            resource_type[resource_type.index("}") + 1 :]
            if "}" in resource_type
            else resource_type
        )

        return cls(
            resource_type=resource_type,
            property_filter=property_filter,
            property_name=property_name,
        )

    @cached_property
    def description(self) -> str:
        if self.property_filter is None:
            return f"All {self.resource_type} resources"
        if isinstance(self.property_filter, Valueset):
            return (
                f"{self.resource_type} filter on Valueset: {self.property_filter.name}"
            )
        if isinstance(self.property_filter, Code):
            return f"{self.resource_type} filter on Code: {self.property_filter.code} {str(self.property_filter.system)}"
        return f"{self.resource_type} filter on list"

    def __hash__(self):
        if self.property_filter is None:
            return hash(self.resource_type)
        if isinstance(self.property_filter, Code):
            return hash((self.resource_type, self.property_filter, self.property_name))

        if isinstance(self.property_filter, Valueset):
            property_filter_hash = hash(tuple(self.property_filter.codes))
        elif isinstance(self.property_filter, list) and isinstance(
            self.property_filter[0], Code
        ):
            property_filter_hash = hash(tuple(self.property_filter))
        elif isinstance(self.property_filter, list) and isinstance(
            self.property_filter[0], Valueset
        ):
            property_filter_hash = hash(
                tuple(
                    [
                        code
                        for valueset in self.property_filter
                        for code in valueset.codes
                    ]
                )
            )
        else:
            raise NotImplementedError(
                f"Unsupported property_filter type: {type(self.property_filter)}"
            )

        return hash((self.resource_type, property_filter_hash, self.property_name))
