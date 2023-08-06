from cqlpy._internal.operators.sort.sort_by_expression import sort_by_expression


def sort_by_column(input_: list, field_name: str, direction: str = "asc") -> list:
    """
    Sorts a list of objects in `input_` according to some field `field_name` in each object.

    ## Parameters

    - `input_`: The list of objects to sort.
    - `field_name`: The name of the field to sort by.
    - `direction`: The direction to sort in. Can be either `"asc"` or `"desc"`.

    ## Returns

    The object list sorted by the field `field_name` in each object.

    ## Example

    ```python
    unsorted = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 20},
    ]
    sorted_ = sort_by_column(unsorted, "age")
    sorted_[0]  # {"name": "Bob", "age": 20}
    ```
    """
    return sort_by_expression([(item[field_name], item) for item in input_], direction)
