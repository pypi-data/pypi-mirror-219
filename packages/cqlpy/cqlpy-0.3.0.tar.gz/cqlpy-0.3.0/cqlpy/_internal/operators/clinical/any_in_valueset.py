# 12.8 In (ValueSet) https://cql.hl7.org/09-b-cqlreference.html#in-valueset


from typing import Union
from cqlpy._internal.operators.clinical.in_valueset import in_valueset
from cqlpy._internal.operators.nullological.is_null import is_null

from cqlpy._internal.types.code import Code
from cqlpy._internal.types.concept import Concept
from cqlpy._internal.types.null import Some
from cqlpy._internal.types.valueset import Valueset

from cqlpy._internal.types.boolean import Boolean


def any_in_valueset(
    argument: list[Some[Union[str, Code, Concept]]], valueset: Valueset
) -> Boolean:
    """
    Returns true if any of the `Code`s or `Concept`s are in the valueset, false otherwise. This is an extension of `in_valueset` to support lists of codes and concepts.

    If `argument` is `Null`, the result is `False`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#in-valueset)

    ## Parameters

    - `argument`: The `Code`s or `Concept`s to check.
    - `valueset`: The `Valueset` to check against.

    ## Returns

    True if any of the `Code`s or `Concept`s are in the valueset, false otherwise.

    ## Usage

    ```python
    codes = ["A00", "A01"]
    any_in_valueset(codes, Valueset("http://hl7.org/fhir/sid/icd-10", codes=["A00"])) # True
    ```
    """
    if not is_null(argument):
        for item in argument:
            if in_valueset(item, valueset):
                return Boolean(True)

    return Boolean(False)
