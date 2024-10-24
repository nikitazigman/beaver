def naive_search(text: str, pattern: str) -> int | None:
    text_index: int = 0
    pattern_index: int = 0

    while text_index < len(text):
        is_characters_equal: bool = text[text_index] == pattern[pattern_index]
        is_the_last_character: bool = pattern_index == len(pattern) - 1

        if is_characters_equal and is_the_last_character:
            return text_index - pattern_index

        if text[text_index] == pattern[pattern_index]:
            pattern_index, text_index = pattern_index + 1, text_index + 1
        else:
            pattern_index, text_index = 0, text_index - (pattern_index - 1)

    return None
