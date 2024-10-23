from heapq import heapify, heappop


def heap_sort(array: list[int]) -> list[int]:
    sorted_array: list[int] = []
    array_copy: list[int] = list(array)
    heapify(array_copy)

    while array_copy:
        sorted_array.append(heappop(array_copy))

    return sorted_array
