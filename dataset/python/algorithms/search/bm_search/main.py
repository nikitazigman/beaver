def boyer_moore_search(text: str, pattern: str) -> int | None:
    if len(text) < len(pattern):
        return None

    pattern_length: int = len(pattern) - 1
    offsets: dict[str, int] = get_offsets(pattern=pattern)

    text_index: int = pattern_length
    pattern_index: int = pattern_length
    count_i: int = pattern_length

    while text_index < len(text):
        if text[text_index] == pattern[pattern_index]:
            if pattern_index == 0:
                return text_index

            text_index, pattern_index = text_index - 1, pattern_index - 1

        else:
            if pattern_index != pattern_length:
                offset: int = offsets[pattern[-1]]
            else:
                offset = offsets.get(text[text_index], pattern_length)

            count_i = text_index = offset + count_i
            pattern_index = pattern_length

    return None


def get_offsets(pattern: str) -> dict[str, int]:
    offsets: dict[str, int] = {}
    for i, char in enumerate(iterable=pattern[:-1]):
        offsets[char] = len(pattern) - i - 1

    offsets.setdefault(pattern[-1], len(pattern))

    return offsets
