from cqlpy._internal.types.any import CqlAny
from cqlpy._internal.types.boolean import Boolean
from cqlpy._internal.types.concept import Concept


def equivalent(left: CqlAny, right: CqlAny) -> Boolean:
    """
    Returns true if the given arguments are equivalent by their Python type. This operator uses unique logic for certain types to determine equivalence, but is generally the same as the `==` operator.

    [Specification](http://cql.hl7.org/09-b-cqlreference.html#equivalent)

    ## Parameters

    - `left`: The left argument.
    - `right`: The right argument.

    ## Returns

    True if the given arguments are equivalent.

    ## Usage

    ```python
    Concept1 = Concept([Code(code="1")])
    Concept2 = Concept([Code(code="1"), Code(code="2")])
    equivalent(Concept1, Concept2)  # True
    ```
    """
    if isinstance(left, Concept) and isinstance(right, Concept):
        return Boolean(
            any(
                code_left.code == code_right.code
                for code_left in left.codes
                for code_right in right.codes
            )
        )
    return Boolean(
        (
            hasattr(left, "value")
            and hasattr(right, "value")
            and (left.value == right.value)
        )
    )
