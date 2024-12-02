def kmp_search(input: str, substr: str) -> int:
    offsets: list[int] = get_offsets(substr=substr)
    j, i = 0, 0

    while i < len(input):
        if input[i] == substr[j] and j == len(substr) - 1:
            return i - j
        elif input[i] == substr[j]:
            i, j = i + 1, j + 1
        elif input[i] != substr[j] and j == 0:
            i += 1
        else:
            j = offsets[j - 1]

    return -1


def get_offsets(substr: str) -> list[int]:
    offsets: list[int] = [0]
    i, j = 1, 0

    while i < len(substr):
        if substr[i] == substr[j]:
            offsets.append(j + 1)
            i, j = i + 1, j + 1
        elif substr[i] != substr[j] and j == 0:
            offsets.append(j)
            i += 1
        else:
            j: int = offsets[j - 1]

    return offsets
