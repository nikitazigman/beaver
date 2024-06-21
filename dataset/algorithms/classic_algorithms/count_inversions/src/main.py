def count_inversions(array, n):
    temp_array = [0] * n
    return _count_inversions_helper(array, temp_array, 0, n - 1)


def _count_inversions_helper(array, temp_array, left, right):

    inversion_count = 0

    if left < right:
        mid = (left + right) // 2
        inversion_count += _count_inversions_helper(
            array, temp_array, left, mid
        )
        inversion_count += _count_inversions_helper(
            array, temp_array, mid + 1, right
        )
        inversion_count += merge_and_count(array, temp_array, left, mid, right)

    return inversion_count


def merge_and_count(array, temp_array, left, mid, right):
    i = left
    j = mid + 1
    k = left
    inversion_count = 0

    while i <= mid and j <= right:

        if array[i] <= array[j]:
            temp_array[k] = array[i]
            k += 1
            i += 1
        else:
            temp_array[k] = array[j]
            inversion_count += mid - i + 1
            k += 1
            j += 1

    while i <= mid:
        temp_array[k] = array[i]
        k += 1
        i += 1

    while j <= right:
        temp_array[k] = array[j]
        k += 1
        j += 1

    for index in range(left, right + 1):
        array[index] = temp_array[index]

    return inversion_count
