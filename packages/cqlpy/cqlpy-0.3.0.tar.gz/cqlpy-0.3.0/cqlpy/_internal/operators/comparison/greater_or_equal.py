from xmlrpc.client import Boolean
from cqlpy._internal.operators.nullological.is_null import is_null
from cqlpy._internal.types.quantity import Quantity


def greater_or_equal(left, right) -> Boolean:
    """
    Returns True if the left argument is greater than or equal to the
    right argument, False otherwise. You may also use the `>=` operator
    to compare two values, though the result will be a Python type.

    [Specification](http://cql.hl7.org/09-b-cqlreference.html#greater-or-equal)

    ## Parameters

    - `left`: The left argument.
    - `right`: The right argument.

    ## Returns

    True if the left argument is greater than or equal to the right
    argument, False otherwise.

    ## Usage

    ```python
    greater_or_equal(Integer(2), Integer(1))  # True
    greater_or_equal(Integer(1), Integer(1))  # True
    ```
    """
    if is_null(left) or is_null(right):
        return Boolean(False)
    else:
        left_value = (
            left["value"]
            if left.__class__.__name__ == "Resource"
            else left.value
            if isinstance(left, Quantity)
            else left
        )
        right_value = (
            right["value"]
            if right.__class__.__name__ == "Resource"
            else right.value
            if isinstance(right, Quantity)
            else right
        )
        return Boolean(left >= right)
