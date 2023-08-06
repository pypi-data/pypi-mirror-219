from cqlpy._internal.types.code import Code
from cqlpy._internal.types.concept import Concept


def to_concept(code: Code) -> Concept:
    """
    Converts a Code to a Concept.

    [Specification](http://cql.hl7.org/09-b-cqlreference.html#toconcept)

    ## Parameters

    - `code`: The `Code` to convert.

    ## Returns

    A `Concept` with the given `Code`.

    ## Usage

    ```python
    code = Code(code="1");
    to_concept(code)
    ```

    """
    return Concept([code])
