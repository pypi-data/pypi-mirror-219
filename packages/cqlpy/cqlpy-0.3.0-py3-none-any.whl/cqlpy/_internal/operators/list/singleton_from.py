from typing import TypeVar
from cqlpy._internal.types.null import Some


_SingletonFromType = TypeVar("_SingletonFromType")


def singleton_from(
    argument: list[Some[_SingletonFromType]],
) -> Some[_SingletonFromType]:
    """
    Returns the single element of the given list.

    If the argument is `Null` or empty, the result is `Null`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#singleton-from)

    ## Parameters

    - `argument`: The list to get the single element of.

    ## Returns

    The single element of the given list.

    ## Usage

    ```python
    singleton_from([1])  # 1
    ```
    """
    # todo: handle situations where there is 0 or 2+ instances in the list
    return argument[0]
