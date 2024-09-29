from heapq import heapify, heappop


def heap_sort(arr):
    sorted_array = []
    arr_copy = arr[:]
    heapify(arr_copy)
    while arr_copy:
        sorted_array.append(heappop(arr_copy))
    return sorted_array
