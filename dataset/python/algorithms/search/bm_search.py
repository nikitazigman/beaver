def bm_search(string, substring):
    assert len(string) >= len(substring)
    offsets = get_offsets(substring)
    i = j = count_i = len(substring) - 1
    while i < len(string):
        if string[i] == substring[j]:
            if j == 0:
                return i
            i -= 1
            j -= 1
        else:
            count_i = i = (
                offsets[substring[-1]]
                if j != len(substring) - 1
                else offsets.get(string[i], len(substring) - 1)
            ) + count_i
            j = len(substring) - 1
    return -1


def get_offsets(substring):
    offsets = {}
    for i, char in enumerate(substring[:-1]):
        offsets[char] = len(substring) - i - 1
    offsets.setdefault(substring[-1], len(substring))
    return offsets
