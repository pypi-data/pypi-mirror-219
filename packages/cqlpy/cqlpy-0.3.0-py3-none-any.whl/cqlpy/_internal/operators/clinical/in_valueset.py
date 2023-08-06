from typing import Union
from cqlpy._internal.operators.nullological.is_null import is_null

from cqlpy._internal.types.code import Code
from cqlpy._internal.types.concept import Concept
from cqlpy._internal.types.null import Some
from cqlpy._internal.types.valueset import Valueset

from cqlpy._internal.types.boolean import Boolean


def in_valueset(
    argument: Some[Union[str, Code, Concept]], valueset: Valueset
) -> Boolean:
    """
    Returns true if the `Code` or `Concept` is in the valueset, false otherwise.

    If `argument` is `Null`, the result is `False`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#in-valueset)

    ## Parameters

    - `argument`: The `Code` or `Concept` to check.
    - `valueset`: The `Valueset` to check against.

    ## Returns

    True if the `Code` or `Concept` is in the valueset, false otherwise.

    ## Usage

    ```python
    in_valueset("A00", Valueset("http://hl7.org/fhir/sid/icd-10", codes=["A00"])) # True
    ```

    """
    if is_null(argument):
        return Boolean(False)

    elif isinstance(argument, str):
        for valueset_code in valueset.codes:
            if argument == valueset_code:
                return Boolean(True)

    elif isinstance(argument, Code):
        for valueset_code in valueset.codes:
            if argument.code == valueset_code.code:
                return Boolean(True)

    elif isinstance(argument, Concept):
        for code in argument.codes:
            for valueset_code in valueset.codes:
                if code.code == valueset_code.code:
                    return Boolean(True)

    return Boolean(False)
