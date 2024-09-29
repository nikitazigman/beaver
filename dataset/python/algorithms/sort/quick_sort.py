import random


def quick_sort(arr):
    copy = arr[:]
    do_sort(copy, 0, len(copy) - 1)
    return copy


def do_sort(arr, left, right):
    if left >= right:
        return
    pivot = arr[(left + right) // 2]
    left_pointer = left
    right_pointer = right
    while left_pointer <= right_pointer:
        while left_pointer <= right_pointer and arr[left_pointer] < pivot:
            left_pointer += 1
        while left_pointer <= right_pointer and arr[right_pointer] > pivot:
            right_pointer -= 1
        if left_pointer <= right_pointer:
            arr[left_pointer], arr[right_pointer] = (
                arr[right_pointer],
                arr[left_pointer],
            )
            left_pointer += 1
            right_pointer -= 1
    do_sort(arr, left, right_pointer)
    do_sort(arr, left_pointer, right)


def quick_sort2(array):
    quick_sort_helper(array, 0, len(array) - 1)
    return array


def quick_sort_helper(array, left, right):
    if left >= right:
        return
    i = partition(array, left, right)
    quick_sort_helper(array, left, i)
    quick_sort_helper(array, i + 1, right)


def partition(array, left, right):
    pivot_index = random.randint(left, right)
    pivot = array[pivot_index]
    array[right], array[pivot_index] = array[pivot_index], array[right]
    i = left
    j = right - 1
    while i < j:
        if array[i] < pivot:
            i += 1
            continue
        if array[j] > pivot:
            j -= 1
            continue
        array[i], array[j] = array[j], array[i]
        i += 1
        j -= 1
    if array[i] >= pivot:
        array[right], array[i] = array[i], array[right]
        return i
    return j
