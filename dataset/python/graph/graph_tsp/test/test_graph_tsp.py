import pytest

from graph_list.src.main import Graph
from graph_tsp.src.main import tsp


@pytest.fixture
def sample_graph():
    g = Graph()
    g.add_vertices(["A", "B", "C", "D"])
    g.add_edges(
        [
            ("A", "B", 1),
            ("A", "C", 3),
            ("A", "D", 4),
            ("B", "C", 2),
            ("B", "D", 3),
            ("C", "D", 1),
        ]
    )
    return g


def test_tsp(sample_graph):
    best_cycle = tsp(sample_graph)
    assert set(best_cycle) == {"A", "B", "C", "D"}
    assert sample_graph.cycle_weight(best_cycle) == min(
        sample_graph.cycle_weight(["A", "B", "C", "D"]),
        sample_graph.cycle_weight(["A", "C", "B", "D"]),
        sample_graph.cycle_weight(["A", "B", "D", "C"]),
        sample_graph.cycle_weight(["A", "D", "C", "B"]),
    )


def test_tsp_small_graph():
    g = Graph()
    g.add_vertices(["A", "B"])
    g.add_edges([("A", "B", 1)])
    best_cycle = tsp(g)
    assert set(best_cycle) == {"A", "B"}
