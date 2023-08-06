def sort_by_direction(input_: list, direction: str = "asc") -> list:
    """
    Sorts a list either ascending or descending.

    ## Parameters

    - `input_`: The list to sort.
    - `direction`: The direction to sort in. Can be either `"asc"` or `"desc"`.

    ## Returns

    The sorted list.

    ## Example

    ```python
    unsorted = [3, 1, 2]
    sorted_ = sort_by_direction(unsorted)
    sorted_  # [1, 2, 3]
    ```
    """
    input_.sort(reverse=(direction == "desc"))
    return input_
