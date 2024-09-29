def merge_sort(arr):

    def merge_arrays(arr1, arr2):
        pointer1 = 0
        pointer2 = 0
        result = []
        while pointer1 < len(arr1) and pointer2 < len(arr2):
            if arr1[pointer1] > arr2[pointer2]:
                result.append(arr2[pointer2])
                pointer2 += 1
            else:
                result.append(arr1[pointer1])
                pointer1 += 1
        while pointer1 < len(arr1):
            result.append(arr1[pointer1])
            pointer1 += 1
        while pointer2 < len(arr2):
            result.append(arr2[pointer2])
            pointer2 += 1
        return result

    if len(arr) <= 1:
        return arr
    mid = int(len(arr) / 2)
    return merge_arrays(merge_sort(arr[:mid]), merge_sort(arr[mid:]))


def merge_sort2(arr):

    def merge_arrays(arr, left1, right1, left2, right2, buffer):
        pointer1 = left1
        pointer2 = left2
        buffer_pointer = left1
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

    def merge_sort(arr, left, right, buffer):
        if left >= right:
            return
        middle = (left + right) // 2
        merge_sort(arr, left, middle, buffer)
        merge_sort(arr, middle+1, right, buffer)
        merge_arrays(arr, left, middle, middle + 1, right, buffer)

    buffer = [None] * len(arr)
    merge_sort(arr, 0, len(arr) - 1, buffer)
    return arr
