import random


def quick_sort2(array: list[int]) -> list[int]:
    quick_sort_helper(array=array, left=0, right=len(array) - 1)
    return array


def quick_sort_helper(array: list[int], left: int, right: int) -> None:
    if left >= right:
        return

    p: int = partition(array=array, left=left, right=right)
    quick_sort_helper(array=array, left=left, right=p)
    quick_sort_helper(array=array, left=p + 1, right=right)


def partition(array: list[int], left: int, right: int) -> int:
    pivot_index: int = random.randint(a=left, b=right)
    pivot: int = array[pivot_index]

    array[right], array[pivot_index] = array[pivot_index], array[right]

    i: int = left
    j: int = right - 1
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
