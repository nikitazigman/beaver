def insertion_sort(array: list[int]) -> list[int]:
    for i in range(len(array)):
        j: int = i
        while j > 0 and array[j] < array[j - 1]:
            array[j], array[j - 1] = array[j - 1], array[j]
            j -= 1

    return array
