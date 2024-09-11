from src.main import naive_search


def test_naive_search_found():
    string = "ABABDABACDABABCABAB"
    substring = "ABABCABAB"
    assert naive_search(string, substring) == 10


def test_naive_search_not_found():
    string = "ABABDABACDABABCABAB"
    substring = "ABCDEF"
    assert naive_search(string, substring) == -1


def test_naive_search_at_start():
    string = "ABABCABAB"
    substring = "ABAB"
    assert naive_search(string, substring) == 0


def test_naive_search_at_end():
    string = "ABABDABACDABABCABAB"
    substring = "CABAB"
    assert naive_search(string, substring) == 14


def test_naive_search_single_char():
    string = "ABABDABACDABABCABAB"
    substring = "D"
    assert naive_search(string, substring) == 4


def test_naive_search_same_string():
    string = "ABABCABAB"
    substring = "ABABCABAB"
    assert naive_search(string, substring) == 0


def test_naive_search_partial_match():
    string = "AABAACAADAABAABA"
    substring = "AABA"
    assert naive_search(string, substring) == 0
