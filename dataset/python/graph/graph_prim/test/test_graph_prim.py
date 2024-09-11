import pytest

from graph_list.src.main import Graph
from graph_prim.src.main import prim


@pytest.fixture
def sample_graph():
    g = Graph()
    g.add_vertices(["A", "B", "C", "D"])
    g.add_edges([("A", "B", 1), ("A", "C", 3), ("B", "C", 1), ("C", "D", 2)])
    return g


def test_prim(sample_graph):
    total_cost, mst = prim(sample_graph)
    assert total_cost == 4
    assert mst.get_all_vertices() == sample_graph.get_all_vertices()
