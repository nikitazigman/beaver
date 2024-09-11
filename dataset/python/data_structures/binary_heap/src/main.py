class BinaryHeap:

    def __init__(self, compare, elements=[]):
        self.compare = compare
        self.values = []
        self.multiple_insert(elements)

    def insert(self, element):
        self.values.append(element)
        self._bubble_up()

    def multiple_insert(self, elements):
        for element in elements:
            self.insert(element)

    def extract(self):
        if len(self.values) == 0:
            return None
        element = self.values[0]
        self._swap(0, -1)
        self.values.pop(-1)
        if len(self.values) > 1:
            self._bubble_down()
        return element

    def _bubble_up(self):
        parent_index = (len(self.values) - 1) // 2
        element_index = len(self.values) - 1
        while (
            self.compare(self.values[parent_index], self.values[element_index])
            and element_index > 0
        ):
            self._swap(parent_index, element_index)
            element_index = parent_index
            parent_index = (parent_index - 1) // 2

    def _bubble_down(self):
        index = 0
        child_to_swap = self._get_child_to_swap(index)
        while child_to_swap != index:
            self._swap(index, child_to_swap)
            index, child_to_swap = child_to_swap, self._get_child_to_swap(
                child_to_swap
            )

    def _swap(self, i, j):
        self.values[i], self.values[j] = self.values[j], self.values[i]

    def _left_child_index(self, parent_index):
        return 2 * parent_index + 1

    def _right_child_index(self, parent_index):
        return 2 * parent_index + 2

    def _children_indexes(self, parent_index):
        return [
            self._left_child_index(parent_index),
            self._right_child_index(parent_index),
        ]

    def _is_valid_index(self, index):
        return 0 <= index < len(self.values)

    def _get_child_to_swap(self, parent_index):
        left_child = self._left_child_index(parent_index)
        right_child = self._right_child_index(parent_index)
        indexes = [parent_index, left_child, right_child]
        valid_indexes = [
            index for index in indexes if self._is_valid_index(index)
        ]
        return self._get_max_element_index(valid_indexes)

    def _get_max_element_index(self, indexes):
        max_element_index = indexes[0]
        for index in indexes:
            if self.compare(
                self.values[max_element_index], self.values[index]
            ):
                max_element_index = index
        return max_element_index
