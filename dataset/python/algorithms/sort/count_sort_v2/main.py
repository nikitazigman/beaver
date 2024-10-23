def count_sort(array: list[int]) -> list[int]:
    if len(array) <= 1:
        return array

    max_element: int = max(array)

    count_map: dict[int, int] = {}
    for element in array:
        count_map[element] = count_map.get(element, 0) + 1

    result_array: list[int] = []
    for i in range(1, max_element + 1):
        if i in count_map:
            result_array.extend([i] * count_map[i])

    return result_array
