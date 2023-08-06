from cqlpy._internal.operators.sort.tuple_sort import tuple_sort


def sort_by_expression(input_: list, direction: str = "asc") -> list:
    """
    Sorts a list of tuples in `input_` according to the first element in each tuple.

    ## Parameters

    - `input_`: The list of tuples to sort.
    - `direction`: The direction to sort in. Can be either `"asc"` or `"desc"`.

    ## Returns

    The object list sorted by the first element in each tuple.

    ## Example

    ```python
    unsorted = [
        (30, 1),
        (20, 2),
    ]
    sorted_ = sort_by_expression(unsorted)
    sorted_[0]  # (20, 2)
    ```
    """
    input_.sort(reverse=(direction == "desc"), key=tuple_sort)
    return [item[1] for item in input_]
