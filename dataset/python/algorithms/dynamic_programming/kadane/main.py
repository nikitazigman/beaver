def kadane(array):
    best_sum = array[0]
    curr_max_sum = array[0]
    for i in range(1, len(array)):
        curr_max_sum = max(array[i], curr_max_sum + array[i])
        best_sum = max(best_sum, curr_max_sum)
    return best_sum
