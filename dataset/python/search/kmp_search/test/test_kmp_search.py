from src.main import kmp_search


def test_kmp_search_found():
    string = "ABABDABACDABABCABAB"
    substring = "ABABCABAB"
    assert kmp_search(string, substring) == 10


def test_kmp_search_not_found():
    string = "ABABDABACDABABCABAB"
    substring = "ABCDEF"
    assert kmp_search(string, substring) == -1


def test_kmp_search_at_start():
    string = "ABABCABAB"
    substring = "ABAB"
    assert kmp_search(string, substring) == 0


def test_kmp_search_single_char():
    string = "ABABDABACDABABCABAB"
    substring = "D"
    assert kmp_search(string, substring) == 4


def test_kmp_search_same_string():
    string = "ABABCABAB"
    substring = "ABABCABAB"
    assert kmp_search(string, substring) == 0


def test_kmp_search_partial_match():
    string = "AABAACAADAABAABA"
    substring = "AABA"
    assert kmp_search(string, substring) == 0
