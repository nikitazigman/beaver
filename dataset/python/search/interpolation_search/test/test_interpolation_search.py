from src.main import interpolation_search


def test_interpolation_search_found():
    array = [10, 20, 30, 40, 50]
    element = 30
    assert interpolation_search(array, element) == 2


def test_interpolation_search_not_found():
    array = [10, 20, 30, 40, 50]
    element = 60
    assert interpolation_search(array, element) == -1


def test_interpolation_search_empty_array():
    array = []
    element = 10
    assert interpolation_search(array, element) == -1


def test_interpolation_search_first_element():
    array = [10, 20, 30, 40, 50]
    element = 10
    assert interpolation_search(array, element) == 0


def test_interpolation_search_last_element():
    array = [10, 20, 30, 40, 50]
    element = 50
    assert interpolation_search(array, element) == 4
