def kmp_search(str, substr):
    offsets = get_offsets(substr)
    j = 0
    i = 0
    while i < len(str):
        if str[i] == substr[j] and j == len(substr) - 1:
            return i - j
        elif str[i] == substr[j]:
            i += 1
            j += 1
        elif str[i] != substr[j] and j == 0:
            i += 1
        else:
            j = offsets[j - 1]
    return -1


def get_offsets(substr):
    offsets = [0]
    i = 1
    j = 0
    while i < len(substr):
        if substr[i] == substr[j]:
            offsets.append(j + 1)
            j += 1
            i += 1
        elif substr[i] != substr[j] and j == 0:
            offsets.append(j)
            i += 1
        else:
            j = offsets[j - 1]
    return offsets
