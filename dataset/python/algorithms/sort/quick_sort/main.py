def quick_sort(array: list[int]) -> list[int]:
    copy: list[int] = list(array)
    do_sort(array=copy, left=0, right=len(copy) - 1)

    return copy


def do_sort(array: list[int], left: int, right: int) -> None:
    if left >= right:
        return

    pivot: int = array[(left + right) // 2]
    left_pointer: int = left
    right_pointer: int = right

    while left_pointer <= right_pointer:
        while left_pointer <= right_pointer and array[left_pointer] < pivot:
            left_pointer += 1

        while left_pointer <= right_pointer and array[right_pointer] > pivot:
            right_pointer -= 1

        if left_pointer <= right_pointer:
            array[left_pointer], array[right_pointer] = (
                array[right_pointer],
                array[left_pointer],
            )
            left_pointer += 1
            right_pointer -= 1

    do_sort(array=array, left=left, right=right_pointer)
    do_sort(array=array, left=left_pointer, right=right)
