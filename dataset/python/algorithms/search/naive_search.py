def naive_search(str, substr):
    i = 0
    j = 0
    while i < len(str):
        if str[i] == substr[j] and j == len(substr) - 1:
            return i - j
        elif str[i] == substr[j]:
            j += 1
            i += 1
        else:
            i -= j - 1
            j = 0
    return -1
