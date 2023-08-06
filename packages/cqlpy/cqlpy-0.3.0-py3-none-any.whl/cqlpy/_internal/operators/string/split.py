from cqlpy._internal.types.string import String
from cqlpy._internal.types.list import List


def split(string_to_split: String, separator: String) -> List[String]:
    """
    Splits the given string into a list of strings using the given separator.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#split)

    ## Parameters

    - `string_to_split`: The string to split.
    - `separator`: The separator to split on.

    ## Returns

    A `List` of `Strings`.

    ## Usage

    ```python
    split(String("Hello, world!"), String(", "))  # List([String("Hello"), String("world!")])
    ```
    """
    return List([String(part) for part in string_to_split.split(separator)])
