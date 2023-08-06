from typing import TypeVar

from cqlpy._internal.types.any import CqlAny
from cqlpy._internal.types.list import List
from cqlpy._internal.types.null import Some

_ListType = TypeVar("_ListType", bound=Some[CqlAny])


def to_list(*args: _ListType) -> List[_ListType]:
    """
    Converts the given arguments to a list.

    ## Parameters

    - `*args`: The arguments to convert to a list.

    ## Returns

    The given arguments as a list.

    ## Usage

    ```python
    to_list(1, 2, 3)  # [1, 2, 3]
    ```
    """
    return List([item for item in args])
