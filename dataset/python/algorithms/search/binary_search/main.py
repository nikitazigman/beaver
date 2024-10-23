def binary_search(array: list[int], element: int) -> int | None:
    left: int = 0
    right: int = len(array) - 1

    while left <= right:
        mid = int((left + right) / 2)

        if mid >= len(array):
            return None
        elif array[mid] == element:
            return mid
        elif array[mid] < element:
            left = mid + 1
        else:
            right = mid - 1

    return None
