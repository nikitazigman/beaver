from src.main import rk_search


def test_rk_search_found():
    string = "ABABDABACDABABCABAB"
    substring = "ABABCABAB"
    assert rk_search(string, substring) == 10


def test_rk_search_not_found():
    string = "ABABDABACDABABCABAB"
    substring = "ABCDEF"
    assert rk_search(string, substring) == -1


def test_rk_search_at_start():
    string = "ABABCABAB"
    substring = "ABAB"
    assert rk_search(string, substring) == 0


def test_rk_search_at_end():
    string = "ABABDABACDABABCABAB"
    substring = "CABAB"
    assert rk_search(string, substring) == 14


def test_rk_search_single_char():
    string = "ABABDABACDABABCABAB"
    substring = "D"
    assert rk_search(string, substring) == 4


def test_rk_search_same_string():
    string = "ABABCABAB"
    substring = "ABABCABAB"
    assert rk_search(string, substring) == 0


def test_rk_search_partial_match():
    string = "AABAACAADAABAABA"
    substring = "AABA"
    assert rk_search(string, substring) == 0
