from heapq import heapify, heappop, heappush


def k_merge(*arrays):
    heap = [(arr[0], 0, arr) for arr in arrays if len(arr) > 0]
    heapify(heap)
    merged_list = []
    while heap:
        value, index, arr = heappop(heap)
        merged_list.append(value)
        new_index = index + 1
        if new_index < len(arr):
            heappush(heap, (arr[new_index], new_index, arr))
    return merged_list
