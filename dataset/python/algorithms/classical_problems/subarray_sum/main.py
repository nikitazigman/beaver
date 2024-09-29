def is_subsum_exist(arr, target):
    if not arr:
        return False
    left = 0
    current_subsum = arr[0]

    for right in range(1, len(arr)):
        while current_subsum > target and left < right - 1:
            current_subsum -= arr[left]
            left += 1

        if current_subsum == target:
            return True

        if right < len(arr):
            current_subsum += arr[right]

    return current_subsum == target
