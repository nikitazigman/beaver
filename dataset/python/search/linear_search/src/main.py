def linear_search(array, element):
    for i in range(0, len(array)):
        if array[i] == element:
            return i
    return -1
