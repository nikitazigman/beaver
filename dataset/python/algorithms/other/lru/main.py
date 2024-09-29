from collections import namedtuple


Node = namedtuple("Node", ["value", "prev", "next"])


class LruDict:
    def __init__(self, maxsize=1000):
        assert maxsize > 0
        self.__dict = {}
        self.__last_updated_key = None
        self.__old_key = None
        self.__maxsize = maxsize

    def add(self, key, value):
        if len(self.__dict) == self.__maxsize:
            self.remove_old()
        self.__dict[key] = Node(value, self.__last_updated_key, None)
        if self.__last_updated_key is not None:
            self.__dict[self.__last_updated_key] = self.__dict[
                self.__last_updated_key
            ]._replace(next=key)
        self.__last_updated_key = key
        if self.__old_key is None and len(self.__dict) > 0:
            self.__old_key = key

    def remove_old(self):
        if self.__old_key is not None:
            old_node = self.__dict[self.__old_key]
            old_key = self.__old_key
            self.__old_key = old_node.next
            if self.__old_key:
                self.__dict[self.__old_key] = self.__dict[
                    self.__old_key
                ]._replace(prev=None)
            del self.__dict[old_key]

            if len(self.__dict) == 0:
                self.__old_key = None
                self.__last_updated_key = None

    def get(self, key):
        node = self.__dict.get(key)
        if node:
            if key != self.__last_updated_key:
                node_prev = node.prev
                node_next = node.next
                self.__dict[self.__last_updated_key] = self.__dict[
                    self.__last_updated_key
                ]._replace(next=key)
                self.__dict[key] = self.__dict[key]._replace(
                    prev=self.__last_updated_key, next=None
                )

                if node_prev is not None:
                    self.__dict[node_prev] = self.__dict[node_prev]._replace(
                        next=node_next
                    )
                    self.__dict[node_next] = self.__dict[node_next]._replace(
                        prev=node_prev
                    )
                else:
                    self.__dict[node_next] = self.__dict[node_next]._replace(
                        prev=None
                    )

                if key == self.__old_key:
                    self.__old_key = node_next

            self.__last_updated_key = key
            return node.value
        return None
