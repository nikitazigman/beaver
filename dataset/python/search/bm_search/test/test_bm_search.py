from src.main import bm_search


def test_bm_search_found():
    string = "HERE IS A SIMPLE EXAMPLE"
    substring = "EXAMPLE"
    assert bm_search(string, substring) == 17


def test_bm_search_not_found():
    string = "HERE IS A SIMPLE EXAMPLE"
    substring = "NOTFOUND"
    assert bm_search(string, substring) == -1


def test_bm_search_at_start():
    string = "EXAMPLE HERE IS A SIMPLE EXAMPLE"
    substring = "EXAMPLE"
    assert bm_search(string, substring) == 0


def test_bm_search_at_end():
    string = "HERE IS A SIMPLE EXAMPLE"
    substring = "EXAMPLE"
    assert bm_search(string, substring) == 17
