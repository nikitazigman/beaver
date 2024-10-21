def count_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr

    max_element: int = max(arr)

    count_map: dict[int, int] = {}
    for element in arr:
        count_map[element] = count_map.get(element, 0) + 1

    result_array: list[int] = []
    for i in range(1, max_element + 1):
        if i in count_map:
            result_array.extend([i] * count_map[i])

    return result_array
