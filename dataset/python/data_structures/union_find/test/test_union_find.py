from src.main import UnionFind1, UnionFind2, UnionFind3, UnionFind4


def test_union_find1():
    uf = UnionFind1([1, 2, 3, 4])
    uf.union(1, 2)
    uf.union(3, 4)
    assert uf.is_same_set(1, 2)
    assert not uf.is_same_set(1, 3)
    uf.union(1, 3)
    assert uf.is_same_set(1, 3)


def test_union_find2():
    uf = UnionFind2([1, 2, 3, 4])
    uf.union(1, 2)
    uf.union(3, 4)
    assert uf.is_same_set(1, 2)
    assert not uf.is_same_set(1, 3)
    uf.union(1, 3)
    assert uf.is_same_set(1, 3)


def test_union_find3():
    uf = UnionFind3([1, 2, 3, 4])
    uf.union(1, 2)
    uf.union(3, 4)
    assert uf.connected(1, 2)
    assert not uf.connected(1, 3)
    uf.union(1, 3)
    assert uf.connected(1, 3)
    assert uf.count() == 1


def test_union_find4():
    uf = UnionFind4([1, 2, 3, 4])
    uf.union(1, 2)
    uf.union(3, 4)
    assert uf.connected(1, 2)
    assert not uf.connected(1, 3)
    uf.union(1, 3)
    assert uf.connected(1, 3)
    assert uf.count() == 1
