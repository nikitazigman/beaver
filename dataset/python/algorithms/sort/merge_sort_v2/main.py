def merge_sort(array: list[int]) -> list[int]:
    def merge_arrays(
        arr: list[int],
        left1: int,
        right1: int,
        left2: int,
        right2: int,
        buffer: list[int],
    ) -> None:
        pointer1: int = left1
        pointer2: int = left2
        buffer_pointer: int = left1

        while pointer1 <= right1 and pointer2 <= right2:
            if arr[pointer1] > arr[pointer2]:
                buffer[buffer_pointer] = arr[pointer2]
                pointer2 += 1
            else:
                buffer[buffer_pointer] = arr[pointer1]
                pointer1 += 1

            buffer_pointer += 1

        while pointer1 <= right1:
            buffer[buffer_pointer] = arr[pointer1]
            pointer1 += 1
            buffer_pointer += 1

        while pointer2 <= right2:
            buffer[buffer_pointer] = arr[pointer2]
            pointer2 += 1
            buffer_pointer += 1

        for i in range(left1, right2 + 1):
            arr[i] = buffer[i]

    def merge_sort(array: list[int], left: int, right: int, buffer: list[int]) -> None:
        if left >= right:
            return

        middle: int = (left + right) // 2

        merge_sort(array=array, left=left, right=middle, buffer=buffer)
        merge_sort(array=array, left=middle + 1, right=right, buffer=buffer)
        merge_arrays(
            arr=array,
            left1=left,
            right1=middle,
            left2=middle + 1,
            right2=right,
            buffer=buffer,
        )

    buffer: list[int] = [0] * len(array)
    merge_sort(array=array, left=0, right=len(array) - 1, buffer=buffer)

    return array
