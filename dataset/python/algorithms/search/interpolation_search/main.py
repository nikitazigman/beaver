def interpolation_search(array, element):
    left = 0
    right = len(array) - 1
    while left <= right and array[left] != array[right]:
        mid = int(
            left
            + (element - array[left])
            * (right - left)
            / (array[right] - array[left])
        )
        if mid >= len(array):
            return -1
        elif array[mid] == element:
            return mid
        elif array[mid] < element:
            left = mid + 1
        else:
            right = mid - 1
    return -1
