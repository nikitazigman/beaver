def linear_search(array: list[int], element: int) -> int | None:
    for i in range(0, len(array)):
        if array[i] == element:
            return i

    return None
