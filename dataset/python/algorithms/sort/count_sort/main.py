def count_sort(arr):
    if len(arr) <= 1:
        return arr
    max_element = max(arr)
    count_map = {}
    for element in arr:
        count_map[element] = count_map.get(element, 0) + 1
    result_array = []
    for i in range(1, max_element + 1):
        if i in count_map:
            result_array.extend([i] * count_map[i])
    return result_array
