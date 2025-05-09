def selection_sort(array: list[int]) -> list[int]:
    for i in range(len(array) - 1):
        current_min: int = i

        for j in range(i + 1, len(array)):
            if array[j] < array[current_min]:
                current_min = j

        array[current_min], array[i] = array[i], array[current_min]

    return array
