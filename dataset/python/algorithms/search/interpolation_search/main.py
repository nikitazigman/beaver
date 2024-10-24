def interpolation_search(array: list[int], element: int) -> int | None:
    left: int = 0
    right: int = len(array) - 1

    def interpolate() -> int:
        pointer_dist: int = right - left
        value_dist: int = array[right] - array[left]
        error_dist: int = element - array[left]

        position: float = left + ((error_dist * pointer_dist) / value_dist)

        return int(position)

    while left <= right and array[left] != array[right]:
        mid: int = interpolate()

        if mid >= len(array):
            return None

        if array[mid] == element:
            return mid

        if array[mid] < element:
            left = mid + 1
        else:
            right = mid - 1

    return None
