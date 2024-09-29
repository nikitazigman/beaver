import pytest

from algorithms.graph.graph_is_acyclic.main import is_acyclic_graph
from algorithms.graph.graph_list.main import Graph


@pytest.fixture
def acyclic_graph():
    g = Graph()
    g.add_vertices(["A", "B", "C", "D"])
    g.add_edges([("A", "B"), ("B", "C"), ("C", "D")])
    return g


@pytest.fixture
def cyclic_graph():
    g = Graph()
    g.add_vertices(["A", "B", "C", "D"])
    g.add_edges([("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")])
    return g


def test_is_acyclic_graph(acyclic_graph):
    assert is_acyclic_graph(acyclic_graph) is True


def test_is_not_acyclic_graph(cyclic_graph):
    assert is_acyclic_graph(cyclic_graph) is False
