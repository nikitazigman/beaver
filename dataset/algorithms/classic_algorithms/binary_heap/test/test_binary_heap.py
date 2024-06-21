import pytest

from algorithms.classic_algorithms.binary_heap.src.main import BinaryHeap


@pytest.mark.parametrize(
    "elements, extract_order, comparator",
    [
        (
            [3, 1, 6, 5, 2, 4],
            [1, 2, 3, 4, 5, 6],
            lambda a, b: a > b,
        ),  # Min-heap
        (
            [3, 1, 6, 5, 2, 4],
            [6, 5, 4, 3, 2, 1],
            lambda a, b: a < b,
        ),  # Max-heap
    ],
)
def test_binary_heap(elements, extract_order, comparator):
    heap = BinaryHeap(comparator, elements)
    extracted_elements = [heap.extract() for _ in range(len(elements))]
    assert extracted_elements == extract_order
