from typing import Any, Optional, Type
from cqlpy._internal.types.any import CqlAny
from cqlpy._internal.types.code import Code
from cqlpy._internal.types.valueset import Valueset


class ValuesetScope:
    """
    Represents named collection of value sets. This is used for some
    value set providers to indicate that the value sets are related in
    some way, usually by provenance.

    This class is not a part of the CQL specification.

    :param valueset_scope_id: The id of the value set scope. This
        must be unique to the provider.
    """

    def __init__(self, valueset_scope_id: Optional[str] = None):
        self.id = valueset_scope_id

    def __str__(self) -> str:
        return "id:" + (self.id or "")
