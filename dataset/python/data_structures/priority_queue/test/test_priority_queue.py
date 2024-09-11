from src.main import PriorityQueue


def test_extract():
    queue = PriorityQueue()
    queue.insert((5, 1))
    queue.insert((6, 5))
    queue.insert((3, 4))
    queue.insert((2, 7))
    queue.insert((1, 10))
    queue.insert((14, 11))
    assert queue.extract() == 14
    assert queue.extract() == 1
    assert queue.extract() == 2
    assert queue.extract() == 6
    assert queue.extract() == 3
    assert queue.extract() == 5


def test_priority_queue_extract_empty():
    pq = PriorityQueue()
    assert pq.extract() is None
