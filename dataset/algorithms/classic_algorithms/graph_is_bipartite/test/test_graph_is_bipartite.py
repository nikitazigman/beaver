import pytest

from algorithms.classic_algorithms.graph_is_bipartite.src.main import (
    is_bipartite,
)
from algorithms.classic_algorithms.graph_list.src.main import Graph


@pytest.fixture
def bipartite_graph():
    g = Graph()
    g.add_vertices(["A", "B", "C", "D"])
    g.add_edges([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")])
    return g


@pytest.fixture
def non_bipartite_graph():
    g = Graph()
    g.add_vertices(["A", "B", "C"])
    g.add_edges([("A", "B"), ("B", "C"), ("C", "A")])
    return g


def test_is_bipartite(bipartite_graph):
    assert is_bipartite(bipartite_graph)[0] is True


def test_is_not_bipartite(non_bipartite_graph):
    assert is_bipartite(non_bipartite_graph)[0] is False
