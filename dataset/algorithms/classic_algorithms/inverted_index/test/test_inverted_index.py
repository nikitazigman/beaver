from algorithms.classic_algorithms.inverted_index.src.main import (
    inverted_index,
    search,
)


def test_inverted_index_basic():
    documents = [
        {'id': 1, 'data': 'the quick brown fox'},
        {'id': 2, 'data': 'jumps over the lazy dog'},
        {'id': 3, 'data': 'the quick blue hare'}
    ]
    index = inverted_index(documents)
    assert index['the'] == {1, 2, 3}
    assert index['quick'] == {1, 3}
    assert index['brown'] == {1}
    assert index['dog'] == {2}

def test_inverted_index_with_stopwords():
    documents = [
        {'id': 1, 'data': 'the quick brown fox'},
        {'id': 2, 'data': 'jumps over the lazy dog'},
        {'id': 3, 'data': 'the quick blue hare'}
    ]
    stopwords = ['the']
    index = inverted_index(documents, stopwords)
    assert 'the' not in index
    assert index['quick'] == {1, 3}
    assert index['brown'] == {1}
    assert index['dog'] == {2}

def test_search_basic():
    documents = [
        {'id': 1, 'data': 'the quick brown fox'},
        {'id': 2, 'data': 'jumps over the lazy dog'},
        {'id': 3, 'data': 'the quick blue hare'}
    ]
    index = inverted_index(documents)
    result = search(index, ['quick', 'the'])
    assert result == {1, 3}

def test_search_no_results():
    documents = [
        {'id': 1, 'data': 'the quick brown fox'},
        {'id': 2, 'data': 'jumps over the lazy dog'},
        {'id': 3, 'data': 'the quick blue hare'}
    ]
    index = inverted_index(documents)
    result = search(index, ['nonexistent'])
    assert result == set()

def test_search_partial_results():
    documents = [
        {'id': 1, 'data': 'the quick brown fox'},
        {'id': 2, 'data': 'jumps over the lazy dog'},
        {'id': 3, 'data': 'the quick blue hare'}
    ]
    index = inverted_index(documents)
    result = search(index, ['quick', 'hare'])
    assert result == {3}
