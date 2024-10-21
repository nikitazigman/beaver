def merge_sort(array: list[int]) -> list[int]:
    def merge_arrays(array1: list[int], array2: list[int]) -> list[int]:
        pointer1: int = 0
        pointer2: int = 0
        result: list[int] = []

        while pointer1 < len(array1) and pointer2 < len(array2):
            if array1[pointer1] > array2[pointer2]:
                result.append(array2[pointer2])
                pointer2 += 1
            else:
                result.append(array1[pointer1])
                pointer1 += 1

        while pointer1 < len(array1):
            result.append(array1[pointer1])
            pointer1 += 1

        while pointer2 < len(array2):
            result.append(array2[pointer2])
            pointer2 += 1

        return result

    if len(array) <= 1:
        return array

    mid = int(len(array) / 2)

    return merge_arrays(
        array1=merge_sort(array=array[:mid]),
        array2=merge_sort(array=array[mid:]),
    )
