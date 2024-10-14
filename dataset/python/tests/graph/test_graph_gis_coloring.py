import pytest

from algorithms.graph.graph_gis_coloring.main import gis
from algorithms.graph.graph_list.main import Graph


@pytest.fixture
def sample_graph():
    g = Graph()
    g.add_vertices(["A", "B", "C", "D"])
    g.add_edges([("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")])
    return g


def test_gis(sample_graph):
    vertices_colors, used_colors_length = gis(sample_graph)
    assert used_colors_length <= 3
    for vertex, color in vertices_colors.items():
        for adjacent in sample_graph.get_vertex_environment(vertex):
            assert vertices_colors[adjacent] != color
