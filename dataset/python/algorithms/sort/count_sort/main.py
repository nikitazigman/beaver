def count_sort(array: list[int]) -> list[int]:
    if len(array) <= 1:
        return array

    min_element: int = min(array)

    normalized_array: list[int] = [i - min_element for i in array]
    max_normalized_element: int = max(normalized_array)

    count_map: list[int] = [0] * (max_normalized_element + 1)
    for i in normalized_array:
        count_map[i] += 1

    result_array: list[int] = []
    for i in range(max_normalized_element + 1):
        result_array.extend([i + min_element] * count_map[i])

    return result_array
