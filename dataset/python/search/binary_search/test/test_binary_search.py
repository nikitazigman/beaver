from src.main import binary_search


def test_search_found():
    array = [10, 20, 30, 40, 50]
    element = 30
    assert binary_search(array, element) == 2


def test_search_not_found():
    array = [10, 20, 30, 40, 50]
    element = 60
    assert binary_search(array, element) == -1


def test_search_empty_array():
    array = []
    element = 10
    assert binary_search(array, element) == -1


def test_search_first_element():
    array = [10, 20, 30, 40, 50]
    element = 10
    assert binary_search(array, element) == 0


def test_search_last_element():
    array = [10, 20, 30, 40, 50]
    element = 50
    assert binary_search(array, element) == 4
