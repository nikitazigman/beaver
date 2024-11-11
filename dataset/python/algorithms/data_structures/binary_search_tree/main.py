class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
            return

        def insert_helper(node):
            if value == node.value:
                raise Exception("All values in BST should be unique!")
            elif value < node.value:
                if node.left is None:
                    node.left = Node(value)
                else:
                    insert_helper(node.left)
            else:
                if node.right is None:
                    node.right = Node(value)
                else:
                    insert_helper(node.right)

        insert_helper(self.root)

    def remove(self, value):
        if self.root is None:
            raise Exception("Tree is empty!")
        node, parent = self.find_node_with_parent(value)
        if node is None:
            return False
        elif node.left is not None and node.right is not None:
            parent_min = node
            min = node.right
            while min.left is not None:
                parent_min = min
                min = min.left
            if parent_min.left == min:
                parent_min.left = min.right
            else:
                parent_min.right = min.right
            node.value = min.value
        elif node.left is None or node.right is None:
            child_name = "right" if node.left is None else "left"
            if parent is None:
                self.root = getattr(node, child_name)
            elif node.value > parent.value:
                parent.right = getattr(node, child_name)
            else:
                parent.left = getattr(node, child_name)
        else:
            parent.remove_child(node)
        return True

    def multiple_insert(self, values=[]):
        for value in values:
            self.insert(value)

    def bypass_order(self):
        if self.root is None:
            return []

        def bypass_order_helper(node):
            result = []
            if node is None:
                return result
            result += bypass_order_helper(node.left)
            result.append(node.value)
            result += bypass_order_helper(node.right)
            return result

        return bypass_order_helper(self.root)

    def bypass_post_order(self):
        if self.root is None:
            return []

        def bypass_post_order_helper(node):
            result = []
            if node is None:
                return result
            result += bypass_post_order_helper(node.right)
            result.append(node.value)
            result += bypass_post_order_helper(node.left)
            return result

        return bypass_post_order_helper(self.root)

    def find_node_with_parent(self, value):
        def find_node_with_parent_helper(node, parent):
            if node is None:
                return [None, None]
            elif node.value == value:
                return [node, parent]
            else:
                parent = node
                node = node.left if node.value > value else node.right
                return find_node_with_parent_helper(node, parent)

        return find_node_with_parent_helper(self.root, None)

    def min(self, index, node=None):
        stack = []
        current = node or self.root
        while len(stack) > 0 or current is not None:
            if current is not None:
                stack.append(current)
                current = current.left
            else:
                current = stack.pop()
                index -= 1
                if index == 0:
                    return current
                current = current.right
        return None

    def height_tree(self, node):
        def height_tree_helper(node):
            if node is None:
                return 0
            return 1 + max(height_tree_helper(node.left), height_tree_helper(node.right))

        return height_tree_helper(node)

    def left_rotation(self, root_value):
        node, node_parent = self.find_node_with_parent(root_value)
        if node is None or node.right is None:
            return
        old_sub_root = node
        node = old_sub_root.right
        old_sub_root.right = node.left
        node.left = old_sub_root
        if node_parent is None:
            self.root = node
        elif node_parent.value < node.value:
            node_parent.right = node
        else:
            node_parent.left = node
        return node

    def right_rotation(self, root_value):
        node, node_parent = self.find_node_with_parent(root_value)
        if node is None or node.left is None:
            return
        old_sub_root = node
        node = old_sub_root.left
        old_sub_root.left = node.right
        node.right = old_sub_root
        if node_parent is None:
            self.root = node
        elif node_parent.value < node.value:
            node_parent.right = node
        else:
            node_parent.left = node
        return node

    def place_in_root(self, value, root):
        if root is None or root.has_no_child():
            return
        node, parent = self.find_node_with_parent(value)
        while not node.has_direct_child(root) and root != node:
            rotate = self.right_rotation if node.value < parent.value else self.left_rotation
            node = rotate(parent.value)
            node, parent = self.find_node_with_parent(node.value)
        return node

    def balance(self):
        def balance_helper(node):
            if node is None:
                return
            count_children = node.count_children()
            if count_children <= 1:
                return
            min_index = int(count_children / 2 + 1)
            min_value = self.min(min_index, node).value
            new_subtree_root = self.place_in_root(min_value, node)
            balance_helper(new_subtree_root.left)
            balance_helper(new_subtree_root.right)

        balance_helper(self.root)

    def is_balanced(self):
        def is_balanced_helper(node):
            if node is None:
                return True
            diff = abs(self.height_tree(node.left) - self.height_tree(node.right))
            if diff > 1:
                return False
            return is_balanced_helper(node.left) and is_balanced_helper(node.right)

        return is_balanced_helper(self.root)

    def __str__(self):
        if self.root is None:
            return "[]"
        queue = [self.root]
        result = []
        while len(queue) > 0:
            current_node = queue.pop(0)
            if current_node is not None:
                result.append(str(current_node))
                queue.extend([current_node.left, current_node.right])
        return str(result)


class Node:
    def __init__(self, value=None, left=None, right=None, parent_node=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent_node = parent_node

    def has_direct_child(self, node):
        return self.left == node or self.right == node

    def has_no_child(self):
        return self.left is None and self.right is None

    def count_children(self):
        def count_children_helper(node):
            if node is None:
                return 0
            return 1 + count_children_helper(node.left) + count_children_helper(node.right)

        return count_children_helper(self.left) + count_children_helper(self.right)

    def remove_child(self, child):
        if self.left == child:
            child.left = None
        else:
            child.right = None

    def set_parent(self, parent_node):
        self.parent_node = parent_node

    def __lt__(self, other):
        return other.value[0] > self.value[0]

    def __str__(self):
        return (
            f"(value={self.value}, "
            f"left={None if not self.left else self.left.value}, "
            f"right={None if not self.right else self.right.value})"
        )
