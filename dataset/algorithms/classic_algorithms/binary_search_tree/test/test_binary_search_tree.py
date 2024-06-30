from algorithms.classic_algorithms.binary_search_tree.src.main import (
    BinarySearchTree,
)


def test_insert_and_bypass_order():
    bst = BinarySearchTree()
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)
    bst.insert(2)
    bst.insert(4)
    assert bst.bypass_order() == [2, 3, 4, 5, 7]

def test_insert_and_bypass_post_order():
    bst = BinarySearchTree()
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)
    bst.insert(2)
    bst.insert(4)
    assert bst.bypass_post_order() == [7, 5, 4, 3, 2]

def test_remove():
    bst = BinarySearchTree()
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)
    bst.insert(2)
    bst.insert(4)
    bst.remove(3)
    assert bst.bypass_order() == [2, 4, 5, 7]

def test_find_node_with_parent():
    bst = BinarySearchTree()
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)
    node, parent = bst.find_node_with_parent(7)
    assert node.value == 7
    assert parent.value == 5

def test_min():
    bst = BinarySearchTree()
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)
    bst.insert(2)
    bst.insert(4)
    assert bst.min(3).value == 4

def test_height_tree():
    bst = BinarySearchTree()
    bst.insert(5)
    bst.insert(3)
    bst.insert(7)
    bst.insert(2)
    bst.insert(4)
    assert bst.height_tree(bst.root) == 3

def test_balance():
    bst = BinarySearchTree()
    bst.multiple_insert([5, 3, 7, 2, 4, 1, 6, 8])
    bst.balance()
    assert bst.is_balanced()
