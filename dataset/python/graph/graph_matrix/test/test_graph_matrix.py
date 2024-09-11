import pytest

from graph_matrix.src.main import Graph


@pytest.fixture
def sample_graph():
    g = Graph(size=5)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)
    return g


def test_add_edge(sample_graph):
    sample_graph.add_edge(3, 4)
    assert sample_graph.is_adjacent_vertexes(3, 4)


def test_remove_edge(sample_graph):
    sample_graph.remove_edge(1, 2)
    assert not sample_graph.is_adjacent_vertexes(1, 2)


def test_is_adjacent_vertexes(sample_graph):
    assert sample_graph.is_adjacent_vertexes(0, 1)
    assert not sample_graph.is_adjacent_vertexes(3, 0)
